from dataclasses import dataclass
from logging import getLogger
from typing import List, Callable, Awaitable, Optional, Dict

from pydantic.main import BaseModel


@dataclass
class ActionHandler:
    name: str
    description: str
    handler: Callable[[], Awaitable]

    async def __call__(self):
        return await self.handler()


class ActionInfo(BaseModel):
    name: str
    description: str


class Action:
    """
    Expose user-defined action as 'button' in UI
    """

    def __init__(self):
        self.__actions: Dict[str, ActionHandler] = {}

    def __call__(self, func: Optional[Callable[[], Awaitable]] = None, *, name: Optional[str] = None,
                 description: Optional[str] = None):
        """
        Decorator that expose function as an action in UI (ex: button)
        """

        def trace_operation(fn: Callable[[], Awaitable]):
            nonlocal name
            nonlocal description

            if name is None:
                name = fn.__qualname__
            if description is None:
                description = "\n".join(line.strip() for line in (fn.__doc__ or '').splitlines()).strip()
            if name in self.__actions:
                old = self.__actions[name]
                getLogger(self.__class__.__qualname__).warning("redefining UI action %r: %s => %s", name,
                                                               old.handler.__qualname__, fn.__qualname__)
            self.__actions[name] = ActionHandler(name=name, description=description, handler=fn)

            return fn

        if func is None:
            return trace_operation
        return trace_operation(func)

    async def invoke(self, name: str) -> bool:
        """
        Invoke action by name or ignore. If handler will raise an error, the error will NOT be suppressed .
        :param name: action name
        :return: true if action invoked
        """
        handler = self.__actions.get(name)
        if handler is None:
            getLogger(self.__class__.__qualname__).warning("attempt to invoke unknown action %r", name)
            return False
        await handler()
        return True

    @property
    def actions(self) -> List[ActionInfo]:
        """
        Copy of list of defined actions prepared for serialization.
        """
        return [ActionInfo(name=x.name, description=x.description) for x in self.__actions.values()]
