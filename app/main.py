# Uncomment this to pass the first stage
import socket


def msg_estrucutura(data):
    data_linea = data.splitlines()
    data_path = data_linea[0].split()

    return data_path[1]


def manejo_respuesta(path, conexion):
    if path == '/':
        conexion.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        conexion.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


def main():
    # crea un servidor socket
    with socket.create_server(("localhost", 4221)) as server_socket:
        # acepta una conexion al socket y un ip
        conexion, direccion = server_socket.accept()
        data = conexion.recv(1024).decode()  # recopila la data de la peticion

        path = msg_estrucutura(data)  # obtenet path
        manejo_respuesta(path, conexion)  # manejar codigo html


if __name__ == "__main__":
    main()
