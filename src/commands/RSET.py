import re

from Command import Command


class RSET(Command):
    def validate_command(self) -> bool:
        # expected pattern: "RSET" CRLF
        pattern = re.compile(r"^RSET\r\n$")
        return True if pattern.match(self.command_string) else False
