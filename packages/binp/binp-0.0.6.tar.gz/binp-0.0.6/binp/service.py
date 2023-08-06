from asyncio import Task, get_event_loop, sleep, CancelledError
from dataclasses import dataclass
from enum import Enum
from logging import getLogger
from typing import Callable, Awaitable, Optional, Dict, List

from pydantic import BaseModel

from binp.events import Emitter


class Status(str, Enum):
    """
    Service life status
    """
    #: service stopped and will not be restarted
    stopped = 'stopped'
    #: service scheduled to start
    starting = 'starting'
    #: service up and running
    running = 'running'
    #: service stopped, is waiting before restart
    restarting = 'restarting'


class Info(BaseModel):
    """
    Service information
    """
    #: service name
    name: str
    #: service description
    description: str
    #: actual service status
    status: Status
    #: is service marked to be started automatically
    autostart: bool
    #: is service has to be restarted automatically
    restart: bool
    #: interval between restarts
    restart_delay: float


@dataclass
class Handler:
    info: Info
    events: Emitter[Info]
    handler: Callable[[], Awaitable]
    task: Optional[Task] = None

    async def __call__(self):
        logger = getLogger('service:' + self.info.name)
        try:
            while True:
                self.info.status = Status.running
                self.events.emit(self.info)
                try:
                    await self.handler()
                except (CancelledError, KeyboardInterrupt):
                    break
                except Exception as ex:
                    logger.warning("service stopped: %v", ex, exc_info=ex)
                if not self.info.restart:
                    break
                self.info.status = Status.restarting
                self.events.emit(self.info)
                await sleep(self.info.restart_delay)
        finally:
            self.info.status = Status.stopped
            self.events.emit(self.info)


class Service:
    """
    Annotate async function as service (background task). Supports automatic (default) and manual start,
    restarts, restarts delays.

    Useful to interact with environment in unpredictable schedule (ex: listen for low-level network requests).

    .. code-block:: python

       from binp import BINP
       from asyncio import sleep

       binp = BINP()

       @binp.service
       async def check_messages():
           while True:
                await sleep(3)
                print("checks")



    For scheduling by time better use `aiocron` instead:

    .. code-block::

        pip install aiocron

    .. highlight:: python
    .. code-block:: python

        from binp import BINP
        from aiocron import crontab

        binp = BINP()

        @crontab("*/5 * * * *")
        @binp.journal
        async def poll_something():
            print("do something every 5 minutes....")

    :Conflicts:

    Services are indexed by name. If multiple services defined with the same name - the old one will be stopped and
     the latest one will be used.

    :Events:

    * ``service_changed`` - when service status changed. Emits Info

    """

    def __init__(self):
        self.service_changed: Emitter[Info] = Emitter()
        self.__services: Dict[str, Handler] = {}

    def __call__(self, func: Optional[Callable[[], Awaitable]] = None, *,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 restart: bool = True,
                 autostart: bool = True,
                 restart_delay: float = 3):
        """
        Mark async function as service
        """

        def register_function(fn: Callable[[], Awaitable]):
            nonlocal name, description

            if name is None:
                name = fn.__qualname__
            if description is None:
                description = "\n".join(line.strip() for line in (fn.__doc__ or '').splitlines()).strip()
            if name in self.__services:
                old = self.__services[name]
                getLogger(self.__class__.__qualname__).warning("redefining service %r: %s => %s", name,
                                                               old.handler.__qualname__, fn.__qualname__)
                if old.task is not None:
                    old.task.cancel()
                    old.task = None

            handler = Handler(
                info=Info(
                    name=name,
                    description=description,
                    status=Status.stopped,
                    autostart=autostart,
                    restart=restart,
                    restart_delay=restart_delay
                ),
                events=self.service_changed,
                handler=fn
            )

            self.__services[name] = handler
            if autostart:
                self.start(name)
            else:
                self.service_changed.emit(handler.info)

            return fn

        if func is None:
            return register_function
        return register_function(func)

    def start(self, name: str):
        """
        Starts single service by name. Does nothing if no such service or service not yet stopped.
        """
        service = self.__services.get(name)
        if service is None:
            return
        if service.info.status != Status.stopped:
            return
        service.info.status = Status.starting
        service.task = get_event_loop().create_task(service())
        self.service_changed.emit(service.info)

    def stop(self, name: str):
        """
        Stops service by name. Does nothing if no such service or service stopped.
        """
        service = self.__services.get(name)
        if service is None or service.info.status == Status.stopped or service.task is None:
            return
        service.task.cancel()

    @property
    def services(self) -> List[Info]:
        """
        List of all services
        """
        return [v.info for v in self.__services.values()]
