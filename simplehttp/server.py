# Example using Python for simplicity

# Server implementation
import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8080)
    server_socket.bind(server_address)
    server_socket.listen(1)

    print(f"Server listening on {server_address}")

    while True:
        connection, client_address = server_socket.accept()
        handle_client(connection)

def handle_client(connection):
    data = connection.recv(1024)
    print(f"Received: {data.decode('utf-8')}")
    connection.sendall(b"HTTP/1.1 200 OK\r\n\r\nHello, World!")
    connection.close()

if __name__ == "__main__":
    start_server()
