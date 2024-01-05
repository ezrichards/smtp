import re

from Command import Command


class DATA(Command):
    def validate_command(self) -> bool:
        # expected pattern: "DATA" CRLF
        pattern = re.compile(r"^DATA\r\n$")
        return True if pattern.match(self.command_string) else False
