import socket


def send_response(connection: socket.socket, message: str) -> None:
    """
    Sends a UTF-8 encoded message to the given
    socket connection. Does not return anything.
    """
    connection.sendall(message.encode("utf-8"))


def read_response(connection: socket.socket) -> str:
    return connection.recv(1024).decode("utf-8")
