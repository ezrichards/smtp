import logging
import colorlog
import socket
import signal
import sys

from codes import SYNTAX_ERROR_COMMAND, REQUESTED_MAIL_ACTION_OK, SERVICE_CLOSING
from commands.EHLO import EHLO
from commands.HELO import HELO

# TODO better SIGINT handling

server_address = (
    "localhost",
    2525,
)  # would normally run on 25, but we would need to be a privileged user for that
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logger = logging.getLogger()


def setup_logger():
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            fmt="[%(asctime)s]%(log_color)s %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "black",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bold",
            },
            datefmt="%Y-%m-%d %H:%M:%S",
        ),
    )

    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.DEBUG)


def signal_handler(sig, frame) -> None:
    print("You pressed Ctrl+C!")
    print(f"[log] Received SIGINT, killing server..")
    server_socket.close()
    sys.exit(0)


def start_server() -> None:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(1)

    print(f"\nSMTP server listening on {server_address[0]}:{server_address[1]}..\n")

    while True:
        connection, client_address = server_socket.accept()
        print(f"[log] Client connecting @ {client_address}")
        handle_client(connection)


def send_response(
    connection: socket.socket, message: str
) -> None:  # TODO param code and message?
    connection.sendall(message.encode("utf-8"))


def read_response(connection: socket.socket) -> str:
    return connection.recv(1024).decode("utf-8")


def handshake_client(connection: socket.socket) -> bool:
    """
    Establishes a connection with the given client socket; the
    server will send a 220 greeting, and expects a EHLO or HELO in return.

    If the server does not receive this greeting, it will send a 501 back
    until a valid EHLO/HELO is sent or until 5 failed attempts are reached.
    Returns whether or not the handshake was successful.
    """

    # 220 greeting MUST come first
    send_response(connection, f"220 {server_address[0]} ESMTP Postfix")

    attempts = 0
    while attempts < 5:
        # read buffer response - should be EHLO/HELO
        data = read_response(connection)

        if data.split()[0] in "EHLO":
            cmd = EHLO(data)
        elif data.split()[0] == "HELO":
            cmd = HELO(data)
        else:
            send_response(connection, "501 Syntax error in parameters or arguments")

        valid = cmd.validate_command()
        if valid:
            send_response(
                connection, "250 Hello, I am glad to meet you"
            )  # TODO include domain (get this from cmd obj?)
            return True
        else:
            send_response(connection, "501 Syntax error in parameters or arguments")

        attempts += 1

    return False


def handle_client(connection: socket.socket) -> None:
    if not handshake_client(connection):
        logger.info(f"Handshake failed for: {connection.getsockname()}")
        connection.close()
        return

    # TODO handle activated session

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
    setup_logger()
    start_server()

    signal.signal(signal.SIGINT, signal_handler)
    print("Press Ctrl+C to end session")
    signal.pause()
