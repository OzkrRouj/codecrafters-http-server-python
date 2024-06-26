# Uncomment this to pass the first stage
import socket
import gzip
from threading import Thread
import binascii

base_directory = "/tmp/data/codecrafters.io/http-server-tester/"


def msg_estrucutura(data):

    data_linea = data.splitlines()  # separar los elementos en lineas
    # separar los elemntos dentro de una linea
    data_path = data_linea[0].split()[1]

    if 'gzip' in data:
        print('OKOKOK')

    data_espacio = data.split()
    # print(data_espacio)
    path_elementos = data_path.split('/')
    data_headers = []
    if data_path == '/user-agent':
        data_headers = data_linea[2].split()[1]
    data_content_post = data_linea[-1]

    # print(data_content_post)
    # print(data_linea)
    # print(data_path)
    # print(data_headers)
    # print(path_elementos)

    return data_path, path_elementos, data_headers, data_content_post, data_linea, data_espacio


def manejo_respuesta(data, estructura, conexion):
    if data.startswith('POST'):
        print('POST-Metodo')
        post_metodo(estructura, conexion)
    elif data.startswith('GET'):
        print('GET-Metodo')
        get_metodo(estructura, conexion, data)


def post_metodo(estructura, conexion):
    if estructura[1][1] == 'files':
        filename = estructura[1][2]
        try:
            filename = estructura[1][2]
            with open(f'/tmp/data/codecrafters.io/http-server-tester/{filename}', 'w') as f:
                filename_content = f.write(estructura[3])
            print(filename_content)
            file_msg = f'HTTP/1.1 201 Created\r\n\r\n'.encode()
            conexion.sendall(file_msg)
        except FileNotFoundError:
            file_msg = b"HTTP/1.1 404 Not Found\r\n\r\n"
            conexion.sendall(file_msg)
            return


def get_metodo(estructura, conexion, data):

    if 'gzip' in data and 'Accept-Encoding' in data:
        echo_element = estructura[1][2]
        print(echo_element)
        content_gzip = gzip.compress(echo_element.encode())
        print(content_gzip)
        contenido_hex = binascii.hexlify(content_gzip).decode('ascii')
        print(contenido_hex)
        echo_msg = f'HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: {len(content_gzip)}\r\n{contenido_hex}'.encode(
        )
        conexion.sendall(echo_msg)
        return

    if estructura[1][1] == 'files':
        filename = estructura[1][2]
        try:
            filename = estructura[1][2]
            with open(f'/tmp//data/codecrafters.io/http-server-tester/{filename}', 'r') as f:
                filename_content = f.read()
            print(filename_content)
            file_msg = f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(filename_content)}\r\n\r\n{filename_content}'.encode(
            )
            conexion.sendall(file_msg)
        except FileNotFoundError:
            file_msg = b"HTTP/1.1 404 Not Found\r\n\r\n"
            conexion.sendall(file_msg)
        return

    if estructura[1][1] == 'echo':
        echo_element = estructura[1][2]
        echo_msg = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_element)}\r\n\r\n{echo_element}'.encode(
        )
        conexion.sendall(echo_msg)
        return
    if estructura[0] == '/user-agent':
        data_header = estructura[2]
        data_msg = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(data_header)}\r\n\r\n{data_header}'.encode(
        )
        conexion.sendall(data_msg)
        return
    if estructura[0] == '/':
        conexion.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        return
    if estructura[0] != '/':
        conexion.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
        return


def manejar_conexion(conexion, direccion):
    data = conexion.recv(1024).decode()  # recopila la data de la peticion
    print(f'DATA - {data}')
    estructura = msg_estrucutura(data)  # obtenet path
    # print(estructura)
    manejo_respuesta(data, estructura, conexion)  # manejar codigo html
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
