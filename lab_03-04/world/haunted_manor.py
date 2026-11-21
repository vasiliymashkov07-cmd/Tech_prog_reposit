from ..core.dice import Dice
from ..enemy.enemy import Enemy
from ..enemy.haunted_weapon import HauntedWeapon
from ..item.default_catalog import IRON_SWORD, ELVEN_BOW, EMBER_STAFF
from ..item.item_catalog import ItemCatalog
from .location import Location


class HauntedManor(Location):
    CODE = "haunted-manor"
    HAUNTED_WEAPONS = (IRON_SWORD, ELVEN_BOW, EMBER_STAFF)

    def __init__(self, catalog: ItemCatalog) -> None:
        super().__init__(self.CODE, "Проклятый особняк", 2, catalog)

    def _create_enemy(self) -> Enemy:
        return HauntedWeapon(self._catalog.create_weapon(Dice().pick(self.HAUNTED_WEAPONS)))

    @property
    def _loot_table(self) -> tuple[str, ...]:
        return self.HAUNTED_WEAPONS
