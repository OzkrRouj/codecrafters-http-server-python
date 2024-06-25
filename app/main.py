# Uncomment this to pass the first stage
import socket
from threading import Thread


def msg_estrucutura(data):
    data_linea = data.splitlines()  # separar los elementos en lineas
    # separar los elemntos dentro de una linea
    data_path = data_linea[0].split()[1]

    path_elementos = data_path.split('/')
    data_headers = []
    if data_path == '/user-agent':
        data_headers = data_linea[2].split()[1]
    print(data_headers)
    print(path_elementos)

    return data_path, path_elementos, data_headers


def manejo_respuesta(path, conexion):

    if path[1][1] == 'files':
        filename = path[1][2]
        try:
            with open(f'/tmp/{filename}', 'r') as f:
                filename_content = f.read()
            print(filename_content)
            file_msg = f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(filename_content)}\r\n\r\n{filename_content}'.encode(
            )

        except:

            # )
            # conexion.sendall(echo_msg)
            print('filename_content')
        conexion.sendall(file_msg)
        return

    if path[1][1] == 'echo':
        echo_element = path[1][2]
        echo_msg = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_element)}\r\n\r\n{echo_element}'.encode(
        )
        conexion.sendall(echo_msg)
        return
    if path[0] == '/user-agent':
        data_header = path[2]
        data_msg = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(data_header)}\r\n\r\n{data_header}'.encode(
        )
        conexion.sendall(data_msg)
        return
    if path[0] == '/':
        conexion.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        return
    if path[0] != '/':
        conexion.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
        return


def manejar_conexion(conexion, direccion):
    data = conexion.recv(1024).decode()  # recopila la data de la peticion

    path = msg_estrucutura(data)  # obtenet path
    print(path)
    manejo_respuesta(path, conexion)  # manejar codigo html
    conexion.close()


def main():
    # crea un servidor socket

    with socket.create_server(("localhost", 4221)) as server_socket:
        # acepta una conexion al socket y un ip
        while True:
            conexion, direccion = server_socket.accept()
            hilo = Thread(target=manejar_conexion, args=(conexion, direccion))
            hilo.start()


if __name__ == "__main__":
    main()
