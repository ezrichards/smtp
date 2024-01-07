import socket

server_address = ("localhost", 2525)

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

        if "DATA" in message:
            response = client_socket.recv(1024).decode("utf-8")

            if response.startswith("354"):
                print("[client-log] begun data session")
                data_session = True
                while data_session:
                    email_data = input()
                    if email_data == "\\r\\n.\\r\\n":  # must escape the char escapes :)
                        client_socket.sendall(email_data.encode("utf-8"))
                        print("[client-log] receieved quit")
                        break
                    client_socket.sendall(email_data.encode("utf-8"))
            else:
                # TODO handle bad case
                pass

        response = client_socket.recv(1024).decode("utf-8")
        print(response)

        message = input()

    client_socket.sendall(message.encode("utf-8"))
    response = client_socket.recv(1024).decode("utf-8")
    print(response)

    client_socket.close()
