from .game_event import GameEvent
from .game_event_type import GameEventType
from .game_event_listener import GameEventListener


# Издатель оповещает подписчиков об игровых событиях.
class GameEventPublisher:
    def __init__(self) -> None:
        # Подписчики сгруппированы по типам событий.
        self._listeners: dict[GameEventType, list[GameEventListener]] = {}

    def subscribe(self, type: GameEventType, listener: GameEventListener) -> None:
        self._listeners.setdefault(type, []).append(listener)

    def unsubscribe(self, type: GameEventType, listener: GameEventListener) -> None:
        # Если подписки нет, удалять ничего не нужно.
        listeners = self._listeners.get(type, [])
        if listener in listeners:
            listeners.remove(listener)

    def publish(self, event: GameEvent) -> None:
        # Перебираем копию списка на случай изменений во время оповещения.
        for listener in tuple(self._listeners.get(event.type, [])):
            listener.on_event(event)
