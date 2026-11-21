from pathlib import Path
from ..camp.merchant import Merchant
from ..combat.outcome import Outcome
from ..core.unknown_code_error import UnknownCodeError
from ..hero.hero import Hero
from ..hero.hero_class import HeroClass
from ..item.default_catalog import (
    create_default_catalog,
    IRON_SWORD,
    ELVEN_BOW,
    EMBER_STAFF,
    CHAINMAIL,
    PLATE_ARMOR,
)
from ..item.item import Item
from ..world.forest import Forest
from ..world.haunted_manor import HauntedManor
from ..world.crypt import Crypt
from ..world.dragon_lair import DragonLair
from ..world.location_registry import LocationRegistry
from ..world.expedition_report import ExpeditionReport
from ..tactic.balanced_tactic import BalancedTactic
from ..tactic.aggressive_tactic import AggressiveTactic
from ..tactic.cautious_tactic import CautiousTactic
from ..tactic.tactic import Tactic
from ..event.game_event import GameEvent
from ..event.game_event_type import GameEventType
from ..event.game_event_publisher import GameEventPublisher
from ..progress.achievement_tracker import AchievementTracker
from ..progress.expedition_journal import ExpeditionJournal
from ..storage.file_hero_repository import FileHeroRepository
from ..storage.caching_hero_repository import CachingHeroRepository


class GameFacade:
    def __init__(self, save_file: Path) -> None:
        self._catalog = create_default_catalog()
        self._locations = LocationRegistry(
            [
                Forest(self._catalog),
                HauntedManor(self._catalog),
                Crypt(self._catalog),
                DragonLair(self._catalog),
            ]
        )
        self.tactics = (BalancedTactic(), AggressiveTactic(), CautiousTactic())
        self._merchant = Merchant(self._catalog, [IRON_SWORD, ELVEN_BOW, EMBER_STAFF, CHAINMAIL, PLATE_ARMOR])
        self._heroes = CachingHeroRepository(FileHeroRepository(save_file, self._catalog))
        self._events = GameEventPublisher()
        self._journal = ExpeditionJournal()
        achievements = AchievementTracker()
        self._events.subscribe(GameEventType.VICTORY, achievements)
        self._events.subscribe(GameEventType.LEVEL_UP, achievements)
        self._events.subscribe(GameEventType.VICTORY, self._journal)
        self._events.subscribe(GameEventType.DEFEAT, self._journal)

    @property
    def hero_classes(self):
        return tuple(HeroClass)

    def get_starter_kit(self, code: str) -> tuple[Item, Item]:
        kit = HeroClass.by_code(code).starter_kit(self._catalog)
        return kit.create_weapon(), kit.create_armor()

    @property
    def locations(self):
        return self._locations.all

    def get_location(self, code: str):
        return self._locations.get(code)

    def get_tactic(self, code: str) -> Tactic:
        for tactic in self.tactics:
            if tactic.code == code:
                return tactic
        raise UnknownCodeError("Тактика", code)

    @property
    def showcase(self):
        return self._merchant.showcase

    def sell_price(self, item: Item) -> int:
        return self._merchant.sell_price(item)

    @property
    def heroes(self) -> list[Hero]:
        return self._heroes.find_all()

    def get_hero(self, name: str) -> Hero:
        hero = self._heroes.find_by_name(name)
        if hero is None:
            raise ValueError("Героя с именем " + name + " нет")
        return hero

    def create_hero(self, name: str, code: str) -> Hero:
        if self._heroes.find_by_name(name) is not None:
            raise ValueError("Герой с именем " + name + " уже есть")
        hero_class = HeroClass.by_code(code)
        hero = (
            Hero.Builder()
            .set_name(name)
            .set_hero_class(hero_class)
            .set_starter_kit(hero_class.starter_kit(self._catalog))
            .build()
        )
        self._heroes.save(hero)
        return hero

    def explore(self, hero_name: str, location_code: str, tactic_code: str) -> ExpeditionReport:
        hero = self.get_hero(hero_name)
        report = self.get_location(location_code).explore(hero, tactic=self.get_tactic(tactic_code))
        result = GameEventType.VICTORY if report.battle.outcome == Outcome.VICTORY else GameEventType.DEFEAT
        self._events.publish(GameEvent(result, hero, report))
        if report.rewards.levels_gained > 0:
            self._events.publish(GameEvent(GameEventType.LEVEL_UP, hero, report))
        self._heroes.save(hero)
        return report

    def equip(self, hero_name: str, index: int) -> Item:
        hero = self.get_hero(hero_name)
        item = hero.inventory[index]
        hero.equip(item)
        self._heroes.save(hero)
        return item

    def buy(self, hero_name: str, code: str) -> Item:
        hero = self.get_hero(hero_name)
        item = self._merchant.buy(hero, code)
        self._heroes.save(hero)
        return item

    def sell(self, hero_name: str, index: int) -> int:
        hero = self.get_hero(hero_name)
        price = self._merchant.sell(hero, hero.inventory[index])
        self._heroes.save(hero)
        return price

    def get_journal(self, name: str):
        return self._journal.get_entries(name)
