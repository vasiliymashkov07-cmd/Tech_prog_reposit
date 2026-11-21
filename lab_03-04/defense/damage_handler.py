from __future__ import annotations
from abc import ABC, abstractmethod
from .damage import Damage


# Базовое звено цепочки защиты.
class DamageHandler(ABC):
    def __init__(self) -> None:
        # Последующее звено может отсутствовать.
        self._next: DamageHandler | None = None

    def set_next(self, handler: DamageHandler) -> DamageHandler:
        self._next = handler
        # Возвращаем следующее звено для удобной сборки цепочки.
        return handler

    @abstractmethod
    def handle(self, damage: Damage) -> None: ...

    def _pass_to_next(self, damage: Damage) -> None:
        # Передаём урон дальше, если цепочка продолжается.
        if self._next is not None:
            self._next.handle(damage)
