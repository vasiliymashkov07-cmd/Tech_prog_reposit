from typing import Protocol
from .game_event import GameEvent


class GameEventListener(Protocol):
    def on_event(self, event: GameEvent) -> None: ...
