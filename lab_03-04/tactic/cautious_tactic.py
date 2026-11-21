from ..combat.combatant import Combatant
from .action import Action
from .tactic import Tactic


# Осторожная тактика для раненого героя.
class CautiousTactic(Tactic):
    @property
    def code(self) -> str:
        # Код используется при выборе тактики.
        return "cautious"

    @property
    def display_name(self) -> str:
        return "Осторожность"

    @property
    def description(self) -> str:
        # Это описание показывается перед экспедицией.
        return "при здоровье ниже 40% через раунд уходить в оборону"

    def choose_action(self, round: int, hero: Combatant, enemy: Combatant) -> Action:
        # Защищаемся на чётных раундах при низком здоровье.
        return Action.DEFEND if hero.health < hero.max_health * 0.4 and round % 2 == 0 else Action.ATTACK
