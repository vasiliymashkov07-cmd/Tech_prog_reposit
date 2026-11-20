from ..hero.hero import Hero
from .hero_repository import HeroRepository


class CachingHeroRepository:
    def __init__(self, target: HeroRepository) -> None:
        self._target = target
        self._cache: dict[str, Hero] | None = None

    def _cached(self) -> dict[str, Hero]:
        if self._cache is None:
            self._cache = {hero.name: hero for hero in self._target.find_all()}
        return self._cache

    def find_by_name(self, name: str) -> Hero | None:
        return self._cached().get(name)

    def find_all(self) -> list[Hero]:
        return list(self._cached().values())

    def save(self, hero: Hero) -> None:
        self._target.save(hero)
        self._cached()[hero.name] = hero
