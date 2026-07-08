from abc import ABC, abstractmethod

class BaseProvider(ABC):
    name = "base"

    @abstractmethod
    def available(self) -> bool:
        pass

    @abstractmethod
    def complete(self, task: dict) -> dict:
        pass
