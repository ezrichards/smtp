# Client implementation
import socket

def send_request():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8080)
    client_socket.connect(server_address)

    message = "GET /path/to/resource HTTP/1.1\r\nHost: localhost\r\nConnection: keep-alive\r\n\r\n"
    client_socket.sendall(message.encode('utf-8'))

    response = client_socket.recv(1024)
    print(f"Received: {response.decode('utf-8')}")

    client_socket.close()

if __name__ == "__main__":
    send_request()
