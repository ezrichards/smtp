import re
import socket

from .Command import Command


class MAIL(Command):
    def validate_command(self) -> bool:
        # expected pattern: "MAIL FROM:" Reverse-path [SP Mail-parameters] CRLF
        pattern = re.compile(r"^MAIL\s+FROM:\s<[^<>]+>\s*(?:\s+[^\s<>]+)?\s*\r\n$")
        return pattern.match(self.command_string) is not None

    def send_valid_response(self, connection: socket.socket) -> None:
        pass

    def send_invalid_response(self, connection: socket.socket) -> None:
        pass
