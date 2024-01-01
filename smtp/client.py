# SMTP Client

import socket

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 2525)
    client_socket.connect(server_address)

    message = "lol client 😂😂\n"
    client_socket.sendall(message.encode('utf-8'))

    response = client_socket.recv(1024)
    print(f"Received: {response.decode('utf-8')}")

    client_socket.close()
