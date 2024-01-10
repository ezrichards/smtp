import re
import socket

from .Command import Command


class RCPT(Command):
    def validate_command(self) -> bool:
        # expected pattern: "RCPT TO:" ( "<Postmaster@" Domain ">" / "<Postmaster>" / Forward-path ) [SP Rcpt-parameters] CRLF
        pattern = re.compile(r"^RCPT\s+TO:\s<[^<>]+>\s*(?:\s+[^\s<>]+)?\s*\r\n$")
        return pattern.match(self.command_string) is not None

    def send_valid_response(self, connection: socket.socket) -> None:
        pass

    def send_invalid_response(self, connection: socket.socket) -> None:
        pass
