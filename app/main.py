# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    with socket.create_server(("localhost", 4221), reuse_port=True) as server_socket:
        conexion, direccion = server_socket.accept()  # wait for client
        print(f"accepted connection from {direccion}")
        data = conexion.recv(1024)
        conexion.sendall(b"HTTP/1.1 200 OK\r\n\r\n")


if __name__ == "__main__":
    main()
