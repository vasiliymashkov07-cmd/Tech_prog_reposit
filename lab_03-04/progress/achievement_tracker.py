from ..event.game_event import GameEvent
from ..event.game_event_type import GameEventType
from .achievement import Achievement


# Подписчик, который открывает достижения героя.
class AchievementTracker:
    def on_event(self, event: GameEvent) -> None:
        hero = event.hero
        if event.type == GameEventType.VICTORY:
            # Первая победа открывает первое достижение.
            hero.unlock(Achievement.FIRST_BLOOD)
            if event.expedition.battle.enemy.code == "dragon":
                hero.unlock(Achievement.DRAGON_SLAYER)
            # Проверяем, нашёл ли герой зачарованную добычу.
            loot = event.expedition.rewards.loot
            if loot is not None and loot.enchantments:
                hero.unlock(Achievement.LUCKY)
        elif event.type == GameEventType.LEVEL_UP and hero.level >= 5:
            # Достижение выдаётся начиная с пятого уровня.
            hero.unlock(Achievement.VETERAN)
