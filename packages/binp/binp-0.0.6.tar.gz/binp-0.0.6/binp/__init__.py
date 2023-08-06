from dataclasses import dataclass, field
from functools import cached_property

from fastapi import FastAPI

from .action import Action
from .api import create_app
from .journals import Journals
from .kv import KV
from .service import Service


@dataclass(frozen=True)
class BINP:
    #: Key-Value default storage
    kv: KV = field(default_factory=KV)
    #: Journal for operation tracing
    journal: Journals = field(default_factory=Journals)
    #: UI exposed actions (buttons)
    action: Action = field(default_factory=Action)
    #: Background services
    service: Service = field(default_factory=Service)

    @cached_property
    def app(self) -> FastAPI:
        """
        Creates FastAPI applications and caches result.
        """
        return create_app(self.journal, self.kv, self.action, self.service)
