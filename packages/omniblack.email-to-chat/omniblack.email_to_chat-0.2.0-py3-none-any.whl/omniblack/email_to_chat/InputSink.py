from abc import ABC, abstractmethod
from asyncio import Queue


class InputSink(ABC):
    def __init__(self):
        self.queue = Queue()

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass
