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


    Expose async function as button to ui.

    It will not be automatically journaled: it's up to you
    add ``@binp.journal`` annotation or not.

    :Example:

    .. code-block:: python

       from binp import BINP
       from asyncio import sleep

       binp = BINP()

       @binp.action
       async def invoke():
           '''
           Do something
           '''
           await sleep(3) # emulate some work
           print("done")

    By default, action will be exposed with name equal to fully-qualified
    function name and description from doc-string (if exists).

    Exposed name could by optionally defined manually.

    .. code-block:: python

       from binp import BINP
       from asyncio import sleep

       binp = BINP()

       @binp.action(name='Do Something', description='Emulate some heavy work')
       async def invoke():
           await sleep(3)
           print("done")


    :Conflicts:

    Actions are indexed by name. If multiple actions defined with the same name - the latest one will be used.
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
        Invoke action by name or ignore. If handler will raise an error, the error will NOT be suppressed.

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
