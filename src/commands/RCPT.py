import re

from .Command import Command


class RCPT(Command):
    def validate_command(self) -> bool:
        # expected pattern: "RCPT TO:" ( "<Postmaster@" Domain ">" / "<Postmaster>" / Forward-path ) [SP Rcpt-parameters] CRLF
        pattern = re.compile(r"^RCPT\s+TO:\s<[^<>]+>\s*(?:\s+[^\s<>]+)?\s*\r\n$")
        return True if pattern.match(self.command_string) else False
