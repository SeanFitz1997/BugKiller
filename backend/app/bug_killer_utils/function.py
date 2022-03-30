import asyncio
from asyncio import AbstractEventLoop
from typing import Awaitable, TypeVar


T = TypeVar('T')


def run_async(future: Awaitable[T]) -> T:
    loop = get_or_create_eventloop()
    return loop.run_until_complete(future)


def get_or_create_eventloop() -> AbstractEventLoop:
    try:
        return asyncio.get_event_loop()
    except RuntimeError as e:
        if 'There is no current event loop in thread' in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()
        else:
            raise
