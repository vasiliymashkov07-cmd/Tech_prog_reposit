from abc import ABC, abstractmethod
from ..combat.combatant import Combatant
from .action import Action


class Tactic(ABC):
    @property
    @abstractmethod
    def code(self) -> str: ...

    @property
    @abstractmethod
    def display_name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def choose_action(self, round: int, hero: Combatant, enemy: Combatant) -> Action: ...
