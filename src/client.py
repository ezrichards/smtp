# SMTP Client

import socket

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 2525)
    client_socket.connect(server_address)

    response = client_socket.recv(1024).decode("utf-8")
    if response.split()[0] == "220":
        print(response)
    else:
        print("BAD RESPONSE!")

    message = input()
    while message != "QUIT":
        message = message + "\r\n"
        client_socket.sendall(message.encode("utf-8"))

        response = client_socket.recv(1024).decode("utf-8")
        print(response)

        message = input()

    client_socket.sendall(message.encode("utf-8"))
    response = client_socket.recv(1024).decode("utf-8")
    print(response)

    client_socket.close()
