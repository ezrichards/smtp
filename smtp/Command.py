from abc import ABC, abstractmethod

class Command(ABC):

    @abstractmethod
    def validate_command(self) -> bool:
        pass
