from __future__ import annotations

from enum import Enum
from ..defense.armor_handler import ArmorHandler
from ..defense.barrier_handler import BarrierHandler
from ..defense.evasion_handler import EvasionHandler
from ..defense.damage_handler import DamageHandler
from ..item.armor import Armor

from ..core.unknown_code_error import UnknownCodeError
from ..item.item_catalog import ItemCatalog
from ..kit.mage_kit_factory import MageKitFactory
from ..kit.ranger_kit_factory import RangerKitFactory
from ..kit.starter_kit_factory import StarterKitFactory
from ..kit.warrior_kit_factory import WarriorKitFactory


class HeroClass(Enum):

    # значение каждого класса: код, название, стартовое здоровье и класс фабрики стартового набора
    WARRIOR = ("warrior", "Воин", 120, WarriorKitFactory)
    RANGER = ("ranger", "Следопыт", 100, RangerKitFactory)
    MAGE = ("mage", "Маг", 85, MageKitFactory)

    def __init__(
        self, code: str, display_name: str, base_health: int, kit_factory: type[StarterKitFactory]
    ) -> None:
        self.code = code
        self.display_name = display_name
        self.base_health = base_health
        self._kit_factory = kit_factory

    # каждый класс сам знает свою фабрику стартового снаряжения
    def starter_kit(self, catalog: ItemCatalog) -> StarterKitFactory:
        return self._kit_factory(catalog)

    @classmethod
    def by_code(cls, code: str) -> HeroClass:
        for hero_class in cls:
            if hero_class.code == code:
                return hero_class

        raise UnknownCodeError("Класс героя", code)

    def create_defense(self, armor: Armor, level: int) -> DamageHandler:
        evasion = 0.15 if self == HeroClass.RANGER else 0.0
        barrier = 30 if self == HeroClass.MAGE else 0
        if self == HeroClass.WARRIOR and level >= 3:
            barrier = 20
        elif self == HeroClass.RANGER and level >= 5:
            barrier = 15
        elif self == HeroClass.MAGE and level >= 3:
            evasion = 0.10
        armor_handler = ArmorHandler(armor.defense)
        first = armor_handler
        if evasion > 0:
            first = EvasionHandler(evasion)
            first.set_next(armor_handler)
        if barrier > 0:
            armor_handler.set_next(BarrierHandler(barrier))
        return first
