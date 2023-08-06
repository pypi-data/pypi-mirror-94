from abc import ABC, abstractmethod
from asyncio import Queue
from enum import Enum, unique
from typing import Union
from collections.abc import Sequence
from dataclasses import dataclass
from textwrap import dedent
from socket import gethostname
from getpass import getuser


@unique
class MessageType(Enum):
    fatal = 'Program encountered a fatal error.'
    error = 'Program encountered an error.'
    report = 'Program reported the results of an execution.'
    heartbeat = 'Program reported it is functioning normally.'


@dataclass
class Message:
    type: MessageType
    program: str
    body: Union[str, Sequence[Sequence[str, str]]]
    host: str
    user: str

    def format_body(self):
        if isinstance(self.body, str):
            return self.body
        else:
            out = ''
            for name, value in self.body:
                out += dedent(f'''
                    ## {name}
                    {value}
                ''')
            return out


@dataclass
class LocalMessage(Message):
    host: str = gethostname()
    user: str = getuser()


class Sink(ABC):
    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass


class InputSink(Sink, ABC):
    def __init__(self):
        self.queue = Queue()


class OutputSink(Sink, ABC):
    @abstractmethod
    async def on_message(self, message: Message) -> None:
        pass


if __name__ == '__main__':
    import code
    code.interact(local=globals())
