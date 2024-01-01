# SMTP Server

import socket

def start_server() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('localhost', 2525) # would normally run on 25, but we would need to be a privileged user for that
    server_socket.bind(server_address)
    server_socket.listen(1)

    print(f"Server listening on {server_address}..")

    while True:
        connection, client_address = server_socket.accept()
        print(f"[log] Client connecting @ {client_address}")
        handle_client(connection)

def handle_client(connection: socket.socket):
    data = connection.recv(1024) # 1 KB buffer
    print(f"Received from client @ {connection.getsockname()}: {data.decode('utf-8')}")
    connection.close()

if __name__ == "__main__":
    start_server()
