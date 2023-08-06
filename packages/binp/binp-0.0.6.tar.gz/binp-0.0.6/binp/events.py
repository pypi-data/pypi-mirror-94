from asyncio import Queue, CancelledError, get_event_loop
from contextlib import contextmanager
from logging import getLogger
from typing import TypeVar, Generic, ContextManager, Set, Awaitable, Callable, Optional

T = TypeVar('T')


class Emitter(Generic[T]):
    """
    Typed event emitter based on async queues.

    Event emitting is non-blocking operation. After subscription, listener will not miss any event regardless
    of processing time (in exchange of memory). Events order are strictly the same as emitting order.

    Can be used as decorator.

    :Example:

    .. code-block:: python

       on_something : Emitter[str] = Emitter()

       @on_something
       async def subscriber(payload: str):
           print("payload:", payload)

       def emitter():
           on_something.emit('hello world')

    Also can be used without decorator

    :Example:

    .. code-block:: python

       on_something : Emitter[str] = Emitter()

       async def subscriber():
           with on_something.subscribe() as queue:
                while True:
                    payload: str = await queue.get()
                    print("payload:", payload)

       def emitter():
           on_something.emit('hello world')

    """

    def __init__(self):
        self.__streams: Set[Queue[T]] = set()

    @contextmanager
    def subscribe(self, own_queue: Optional['Queue[T]'] = None) -> ContextManager['Queue[T]']:
        """
        Create queue that will listen for the event. Queue will be automatically unsubscribed.
        A new queue will be created if no own queue will be provided.
        """
        queue: Queue[T] = own_queue or Queue()
        self.__streams.add(queue)
        try:
            yield queue
        finally:
            self.__streams.remove(queue)

    def emit(self, payload: T):
        """
        Emit event. Non-blocking operation.
        """
        for stream in self.__streams:
            stream.put_nowait(payload)

    def __call__(self, func: Callable[[T], Awaitable]):
        """
        Decorator for async function that will be used as permanent subscriber.

        Important: event listener will be created on next event loop tick.

        Exceptions (except KeyboardInterruption and CancelledError) will be caught and reported to log.
        """

        async def listener():
            logger = getLogger('event:' + func.__qualname__)
            with self.subscribe() as queue:
                payload = await queue.get()
                try:
                    await func(payload)
                except (KeyboardInterrupt, CancelledError):
                    raise
                except Exception as ex:
                    logger.warning("failed to process event: %v", ex, exc_info=ex)

        get_event_loop().create_task(listener())
        return func
