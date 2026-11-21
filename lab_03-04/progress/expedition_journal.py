from ..event.game_event import GameEvent
from ..world.expedition_report import ExpeditionReport


class ExpeditionJournal:
    def __init__(self) -> None:
        self._entries: dict[str, list[ExpeditionReport]] = {}

    def on_event(self, event: GameEvent) -> None:
        self._entries.setdefault(event.hero.name, []).append(event.expedition)

    def get_entries(self, hero_name: str) -> tuple[ExpeditionReport, ...]:
        return tuple(self._entries.get(hero_name, []))
