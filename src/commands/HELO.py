import re

from .Command import Command


class HELO(Command):
    def validate_command(self) -> bool:
        # expected pattern: "EHLO" SP ( Domain / address-literal ) CRLF
        pattern = re.compile(r"^HELO [a-zA-Z0-9.-]+(\.[a-zA-Z]{2,}){1,2}\r\n$")
        return True if pattern.match(self.command_string) else False
