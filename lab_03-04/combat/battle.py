from __future__ import annotations

from .battle_event import BattleEvent
from .battle_report import BattleReport
from .combatant import Combatant
from .event_type import EventType
from .outcome import Outcome
from .participant import Participant
from .side import Side
from ..tactic.action import Action
from ..tactic.tactic import Tactic
from ..tactic.balanced_tactic import BalancedTactic


# бой идет по раундам: сначала бьет герой, потом враг, пока кто-то не погибнет
class Battle:

    def __init__(self, hero: Combatant, enemy: Combatant, tactic: Tactic | None = None) -> None:
        self._hero = hero
        self._tactic = tactic if tactic is not None else BalancedTactic()
        self._enemy = enemy
        self._events: list[BattleEvent] = []
        self._round = 0

    def run(self) -> BattleReport:
        while self._hero.is_alive() and self._enemy.is_alive():
            self._round += 1
            action = self._tactic.choose_action(self._round, self._hero, self._enemy)
            if action == Action.POWER_STRIKE:
                self._emit(BattleEvent(self._round, EventType.POWER_STRIKE, Side.HERO, Side.ENEMY, 0, 0))
            elif action == Action.DEFEND:
                self._emit(BattleEvent(self._round, EventType.DEFEND, Side.HERO, Side.HERO, 0, 0))
            self._strike(self._hero, Side.HERO, self._enemy, Side.ENEMY, action.attack_multiplier)
            if self._enemy.is_alive():
                self._strike(self._enemy, Side.ENEMY, self._hero, Side.HERO, action.incoming_multiplier)

        outcome = Outcome.VICTORY if self._hero.is_alive() else Outcome.DEFEAT
        return BattleReport(
            Participant.of(self._hero), Participant.of(self._enemy), outcome, tuple(self._events)
        )

    def _strike(
        self, attacker: Combatant, source: Side, defender: Combatant, target: Side, multiplier: float
    ) -> None:
        hit = attacker.roll_damage()
        damage = defender.receive_hit(max(1, int(hit.damage * multiplier + 0.5)))
        if damage.evaded:
            self._emit(BattleEvent(self._round, EventType.EVADE, source, target, 0, defender.health))
            return
        if damage.absorbed > 0:
            self._emit(
                BattleEvent(self._round, EventType.ABSORB, source, target, damage.absorbed, defender.health)
            )
        if damage.amount > 0:
            event_type = EventType.CRITICAL_HIT if hit.critical else EventType.HIT
            self._emit(BattleEvent(self._round, event_type, source, target, damage.amount, defender.health))

        if not defender.is_alive():
            self._emit(BattleEvent(self._round, EventType.DEATH, source, target, 0, 0))

    def _emit(self, event: BattleEvent) -> None:
        self._events.append(event)
