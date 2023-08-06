from asyncio import Queue as _Queue


class Queue(_Queue):
    async def __anext__(self):
        return await self.get()

    def __aiter__(self):
        return self
