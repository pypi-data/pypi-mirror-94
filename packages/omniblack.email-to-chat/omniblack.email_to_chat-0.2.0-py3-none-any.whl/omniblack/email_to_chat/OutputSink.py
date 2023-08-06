from abc import abstractmethod, ABC
from email import message


class OutputSink(ABC):
    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass

    @abstractmethod
    async def on_message(self, message: message) -> None:
        pass
