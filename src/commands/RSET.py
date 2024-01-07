import re
import socket

from .Command import Command


class RSET(Command):
    def validate_command(self) -> bool:
        # expected pattern: "RSET" CRLF
        pattern = re.compile(r"^RSET\r\n$")
        return True if pattern.match(self.command_string) else False

    def send_valid_response(self, connection: socket.socket) -> None:
        pass

    def send_invalid_response(self, connection: socket.socket) -> None:
        pass
