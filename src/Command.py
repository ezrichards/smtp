from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, command_string) -> None:
        self.command_string = command_string

    @abstractmethod
    def validate_command(self) -> bool:
        pass
