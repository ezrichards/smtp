import re

from .Command import Command


class EHLO(Command):
    def validate_command(self) -> bool:
        # expected pattern: "EHLO" SP ( Domain / address-literal ) CRLF
        pattern = re.compile(
            r"^EHLO [a-zA-Z0-9.-]+(\.[a-zA-Z]{2,}){1,2}|(\[[a-fA-F0-9:]+\])\r\n$"
        )
        return True if pattern.match(self.command_string) else False
