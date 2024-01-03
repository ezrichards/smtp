import re

from Command import Command


class EHLO(Command):
    def validate_command(self) -> bool:
        # expected pattern: "EHLO" SP ( Domain / address-literal ) CRLF
        pattern = re.compile(r"^EHLO [^\s]+(?:\.[^\s]+)*\r\n$")
        return True if pattern.match(self.command_string) else False
