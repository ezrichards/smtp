import socket
import signal
import sys

from common.logger import setup_logger, logger
from common.sockets import read_response, send_response
from codes import SYNTAX_ERROR_COMMAND, REQUESTED_MAIL_ACTION_OK, SERVICE_CLOSING
from commands.EHLO import EHLO
from commands.HELO import HELO

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

    print(f"\nSMTP server listening on {server_address[0]}:{server_address[1]}..\n")

    while True:
        connection, client_address = server_socket.accept()
        print(f"[log] Client connecting @ {client_address}")
        handle_client(connection)


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

        if data.split()[0] == "EHLO":
            cmd = EHLO(data)
        elif data.split()[0] == "HELO":
            cmd = HELO(data)
        else:
            send_response(connection, "501 Syntax error in parameters or arguments")
            continue

        valid = cmd.validate_command()
        if valid:
            send_response(
                connection, "250 Hello, I am glad to meet you"
            )  # TODO include domain (get this from cmd obj?)
            # TODO do validation inside of the command class and send a response there
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

    # Handshake completed, waiting for next client command
    session_active = True
    data = read_response(connection)

    try:
        while session_active:
            if data.split()[0] == "QUIT":
                logger.info(
                    f"Quit received, terminating connection for {connection.getsockname()}.."
                )
                send_response(connection, f"{SERVICE_CLOSING[0]} Bye")
                session_active = False
                break
            elif data.split()[0] == "DATA":
                # TODO validate data command

                send_response(connection, "354 End data with <CR><LF>.<CR><LF>")

                # store email contents line-by-line
                email_contents = []
                data_session = True

                while data_session:
                    email_data = read_response(connection)

                    logger.debug("received email data " + repr(email_data))

                    if email_data == "\\r\\n.\\r\\n":
                        logger.debug("Received quit signal for DATA call..")
                        send_response(connection, "250 Ok")
                        break
                    email_contents.append(email_data)

                logger.debug("contents after email data session:" + email_contents)
            else:
                send_response(
                    connection, f"{SYNTAX_ERROR_COMMAND[0]} {SYNTAX_ERROR_COMMAND[1]}"
                )

            data = read_response(connection)
    except KeyboardInterrupt:
        print("CTRL-C received in interrupt. Shutting down..")
        server_socket.close()
        sys.exit(0)

    connection.close()


if __name__ == "__main__":
    setup_logger()
    start_server()

    signal.signal(signal.SIGINT, signal_handler)
    print("Press Ctrl+C to end session")
    signal.pause()
