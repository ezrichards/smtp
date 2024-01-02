# SMTP Server

import socket
from codes import SYNTAX_ERROR_COMMAND, REQUESTED_MAIL_ACTION_OK, SERVICE_CLOSING

def validate_command(command: str) -> bool:
    spl = command.lower().split()
    if len(spl) < 1:
        return False
    
    if len(spl[0]) != 4:
        return False

    return True

server_address = ('localhost', 2525) # would normally run on 25, but we would need to be a privileged user for that

def start_server() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(1)

    print(f"[log] SMTP Server listening on {server_address}..")

    while True:
        connection, client_address = server_socket.accept()
        print(f"[log] Client connecting @ {client_address}")
        handle_client(connection)

def handle_client(connection: socket.socket) -> None:
    # 220 greeting MUST come first
    message = f'220 {server_address[0]} ESMTP Postfix'
    connection.sendall(message.encode('utf-8'))

    data = connection.recv(1024).decode('utf-8') # 1 KB buffer
    print(f"[log] Received from client @ {connection.getsockname()}: {data}")

    session_active = True
    while session_active:
        if validate_command(data):
            print(f"[log] Valid command in data: {data}")

            if data.split()[0] == "QUIT":
                print("[log] quit received, terminating connection..")
                connection.sendall(f'{SERVICE_CLOSING[0]} Bye'.encode('utf-8'))
                session_active = False
                break

            # TODO validate EHLO parameters
            domain = data.split()[1]

            message = f'{REQUESTED_MAIL_ACTION_OK[0]} Hello {domain}, I am glad to meet you'
            connection.sendall(message.encode('utf-8'))
        else: 
            message = f'{SYNTAX_ERROR_COMMAND[0]} {SYNTAX_ERROR_COMMAND[1]}'
            connection.sendall(message.encode('utf-8'))

        data = connection.recv(1024).decode('utf-8')

    connection.close()

if __name__ == "__main__":
    start_server()
