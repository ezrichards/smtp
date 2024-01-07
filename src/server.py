import os
import socket
import sys

from dotenv import load_dotenv
from common.logger import setup_logger, logger
from common.sockets import read_response, send_response
from codes import SYNTAX_ERROR_COMMAND, REQUESTED_MAIL_ACTION_OK, SERVICE_CLOSING
from commands.Command import Command
from commands.EHLO import EHLO
from commands.HELO import HELO

load_dotenv()

SERVER_ADDRESS = (
    os.getenv("SERVER_ADDRESS", "localhost"),
    int(os.getenv("SERVER_PORT", 2525)),
)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def shutdown() -> None:
    """
    Ends the server and cleans up server sockets beforehand.
    """
    logger.info(f"Received SIGINT, killing server..")
    server_socket.close()
    sys.exit(0)


def start_server() -> None:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(1)

    print(f"\nSMTP server listening on {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}..\n")

    try:
        while True:
            connection, client_address = server_socket.accept()
            logger.debug(f"Client connecting from: {client_address}..")
            handle_client(connection)
    except KeyboardInterrupt:
        shutdown()


def handshake_client(connection: socket.socket) -> bool:
    """
    Establishes a connection with the given client socket; the
    server will send a 220 greeting, and expects a EHLO or HELO in return.

    If the server does not receive this greeting, it will send a 501 back
    until a valid EHLO/HELO is sent or until 5 failed attempts are reached.
    Returns whether or not the handshake was successful.
    """

    # 220 greeting MUST come first
    send_response(connection, f"220 {SERVER_ADDRESS[0]} ESMTP Postfix")

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

        valid: Command = cmd.validate_command()
        if valid:
            cmd.send_valid_response(connection)
            return True
        else:
            cmd.send_invalid_response(connection)

        attempts += 1

    return False


def handle_client(connection: socket.socket) -> None:
    """
    Handle client connections on the given socket. An attempt will
    first be made to handshake the client; if the client and server cannot perform
    the handshake, the connection will be closed and nothing more will happen.
    """
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

                logger.debug("contents after email data session %s", email_contents)
            else:
                send_response(
                    connection, f"{SYNTAX_ERROR_COMMAND[0]} {SYNTAX_ERROR_COMMAND[1]}"
                )

            data = read_response(connection)
    except KeyboardInterrupt:
        shutdown()

    connection.close()


if __name__ == "__main__":
    setup_logger()
    start_server()
