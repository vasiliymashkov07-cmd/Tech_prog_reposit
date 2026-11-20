import json
from pathlib import Path
from ..hero.hero import Hero
from ..hero.hero_class import HeroClass
from ..item.item import Item
from ..item.item_catalog import ItemCatalog
from ..item.enchantment import by_code
from ..progress.achievement import Achievement


class FileHeroRepository:
    def __init__(self, file: Path, catalog: ItemCatalog) -> None:
        self._file = file
        self._catalog = catalog

    def find_by_name(self, name: str) -> Hero | None:
        return next((hero for hero in self.find_all() if hero.name == name), None)

    def find_all(self) -> list[Hero]:
        if not self._file.exists():
            return []
        text = self._file.read_text(encoding="utf-8")
        if not text.strip():
            return []
        saves = json.loads(text)
        if not isinstance(saves, list):
            raise ValueError("В файле должен быть массив героев")
        return [self._restore(save) for save in saves]

    def save(self, hero: Hero) -> None:
        saves = [self._snapshot(other) for other in self.find_all() if other.name != hero.name]
        saves.append(self._snapshot(hero))
        self._file.parent.mkdir(parents=True, exist_ok=True)
        self._file.write_text(json.dumps(saves, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _snapshot_item(self, item: Item) -> dict:
        return {"code": item.code, "enchantments": [enchantment.code for enchantment in item.enchantments]}

    def _snapshot(self, hero: Hero) -> dict:
        return {
            "name": hero.name,
            "heroClass": hero.hero_class.code,
            "level": hero.level,
            "experience": hero.experience,
            "gold": hero.gold,
            "weapon": self._snapshot_item(hero.weapon),
            "armor": self._snapshot_item(hero.armor),
            "inventory": [self._snapshot_item(item) for item in hero.inventory],
            "achievements": [achievement.code for achievement in hero.achievements],
        }

    def _restore_item(self, save: dict) -> Item:
        item = self._catalog.create(save["code"])
        for code in save["enchantments"]:
            item.enchant(by_code(code))
        return item

    def _restore(self, save: dict) -> Hero:
        return (
            Hero.Builder()
            .set_name(save["name"])
            .set_hero_class(HeroClass.by_code(save["heroClass"]))
            .set_level(save["level"])
            .set_experience(save["experience"])
            .set_gold(save["gold"])
            .set_weapon(self._restore_item(save["weapon"]))
            .set_armor(self._restore_item(save["armor"]))
            .set_inventory([self._restore_item(item) for item in save["inventory"]])
            .set_achievements([Achievement.by_code(code) for code in save["achievements"]])
            .build()
        )
