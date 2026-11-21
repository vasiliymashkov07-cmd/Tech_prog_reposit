from ..combat.combatant import Combatant
from .action import Action
from .tactic import Tactic


class CautiousTactic(Tactic):
    @property
    def code(self) -> str:
        return "cautious"

    @property
    def display_name(self) -> str:
        return "Осторожность"

    @property
    def description(self) -> str:
        return "при здоровье ниже 40% через раунд уходить в оборону"

    def choose_action(self, round: int, hero: Combatant, enemy: Combatant) -> Action:
        return Action.DEFEND if hero.health < hero.max_health * 0.4 and round % 2 == 0 else Action.ATTACK
