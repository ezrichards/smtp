import re

from .Command import Command


class MAIL(Command):
    def validate_command(self) -> bool:
        # expected pattern: "MAIL FROM:" Reverse-path [SP Mail-parameters] CRLF
        pattern = re.compile(r"^MAIL\s+FROM:\s<[^<>]+>\s*(?:\s+[^\s<>]+)?\s*\r\n$")
        return True if pattern.match(self.command_string) else False
