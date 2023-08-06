from dataclasses import dataclass, field
from functools import cached_property

from fastapi import FastAPI

from .action import Action
from .api import create_app
from .journals import Journals
from .kv import KV


@dataclass(frozen=True)
class BINP:
    kv: KV = field(default_factory=KV)
    journal: Journals = field(default_factory=Journals)
    action: Action = field(default_factory=Action)

    @cached_property
    def app(self) -> FastAPI:
        return create_app(self.journal, self.kv, self.action)
