import socket

from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, command_string: str) -> None:
        self.command_string = command_string

    @abstractmethod
    def validate_command(self) -> bool:
        pass

    @abstractmethod
    def send_valid_response(self, connection: socket.socket) -> None:
        pass

    @abstractmethod
    def send_invalid_response(self, connection: socket.socket) -> None:
        pass
