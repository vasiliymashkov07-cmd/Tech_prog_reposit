from ..combat.hit import Hit
from .enemy_decorator import EnemyDecorator


class LegendaryEnemy(EnemyDecorator):
    @property
    def name(self) -> str:
        return "Легендарный " + super().name

    def roll_damage(self) -> Hit:
        hit = super().roll_damage()
        return Hit(hit.damage * 2, hit.critical)

    @property
    def experience_reward(self) -> int:
        return super().experience_reward * 2

    def roll_gold_reward(self) -> int:
        return super().roll_gold_reward() * 2
