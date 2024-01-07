import socket
import re

from common.sockets import send_response
from .Command import Command


class EHLO(Command):
    def validate_command(self) -> bool:
        # expected pattern: "EHLO" SP ( Domain / address-literal ) CRLF
        pattern = re.compile(
            r"^EHLO [a-zA-Z0-9.-]+(\.[a-zA-Z]{2,}){1,2}|(\[[a-fA-F0-9:]+\])\r\n$"
        )
        return True if pattern.match(self.command_string) else False

    def send_valid_response(self, connection: socket.socket) -> None:
        domain = self.command_string.split()[-1]
        send_response(connection, f"250 Hello {domain}, I am glad to meet you")

    def send_invalid_response(self, connection: socket.socket) -> None:
        send_response(connection, "501 Syntax error in parameters or arguments")
        # TODO abstract codes out in case they change
