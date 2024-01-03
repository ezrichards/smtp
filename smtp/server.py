# SMTP Server

import socket
import signal
import sys

from codes import SYNTAX_ERROR_COMMAND, REQUESTED_MAIL_ACTION_OK, SERVICE_CLOSING
from commands.EHLO import EHLO

server_address = (
    "localhost",
    2525,
)  # would normally run on 25, but we would need to be a privileged user for that
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def signal_handler(sig, frame) -> None:
    print("You pressed Ctrl+C!")
    print(f"[log] Received SIGINT, killing server..")
    server_socket.close()
    sys.exit(0)


def start_server() -> None:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(1)

    print(f"[log] SMTP Server listening on {server_address}..")

    while True:
        connection, client_address = server_socket.accept()
        print(f"[log] Client connecting @ {client_address}")
        handle_client(connection)


def send_response(
    connection: socket.socket, message: str
) -> None:  # TODO param code and message?
    connection.sendall(message.encode("utf-8"))


def handle_client(connection: socket.socket) -> None:
    # 220 greeting MUST come first
    send_response(connection, f"220 {server_address[0]} ESMTP Postfix")

    data = connection.recv(1024).decode("utf-8")  # 1 KB buffer
    print(
        f"[log] Received opening socket from client @ {connection.getsockname()}: {data}"
    )

    if data.split()[0] == "EHLO":
        cmd = EHLO(data)
        valid = cmd.validate_command()
        print(valid)

    session_active = True

    try:
        while session_active:
            print(
                f"[log] Received session socket from client @ {connection.getsockname()}: {data}"
            )

            if True:  # TODO per-command validation
                # if validate_command(data):
                print(f"[log] Valid command in data: {data}")

                if data.split()[0] == "QUIT":
                    print("[log] quit received, terminating connection..")
                    connection.sendall(f"{SERVICE_CLOSING[0]} Bye".encode("utf-8"))
                    session_active = False
                    break

                # TODO validate EHLO parameters
                domain = data.split()[1]

                message = f"{REQUESTED_MAIL_ACTION_OK[0]} Hello {domain}, I am glad to meet you"
                connection.sendall(message.encode("utf-8"))
            else:
                message = f"{SYNTAX_ERROR_COMMAND[0]} {SYNTAX_ERROR_COMMAND[1]}"
                connection.sendall(message.encode("utf-8"))

            data = connection.recv(1024).decode("utf-8")
    except KeyboardInterrupt:
        print("CTRL-C received in interrupt. Shutting down...")
        # Perform cleanup operations here
        server_socket.close()
        sys.exit(0)

    connection.close()


if __name__ == "__main__":
    start_server()

    signal.signal(signal.SIGINT, signal_handler)
    print("Press Ctrl+C to end session")
    signal.pause()
