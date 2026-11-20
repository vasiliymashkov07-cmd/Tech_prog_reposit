from __future__ import annotations
from abc import ABC, abstractmethod
from .damage import Damage


class DamageHandler(ABC):
    def __init__(self) -> None:
        self._next: DamageHandler | None = None

    def set_next(self, handler: DamageHandler) -> DamageHandler:
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, damage: Damage) -> None: ...

    def _pass_to_next(self, damage: Damage) -> None:
        if self._next is not None:
            self._next.handle(damage)
