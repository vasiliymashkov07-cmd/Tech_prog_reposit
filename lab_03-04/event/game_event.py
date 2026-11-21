from dataclasses import dataclass
from ..hero.hero import Hero
from ..world.expedition_report import ExpeditionReport
from .game_event_type import GameEventType


@dataclass(frozen=True)
class GameEvent:
    type: GameEventType
    hero: Hero
    expedition: ExpeditionReport
