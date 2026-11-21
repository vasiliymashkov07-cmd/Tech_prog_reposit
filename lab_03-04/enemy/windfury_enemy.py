from ..combat.hit import Hit
from .enemy_decorator import EnemyDecorator


class WindfuryEnemy(EnemyDecorator):
    @property
    def name(self) -> str:
        return "Неистовый " + super().name

    def roll_damage(self) -> Hit:
        first, second = super().roll_damage(), super().roll_damage()
        return Hit(first.damage + second.damage, first.critical or second.critical)

    @property
    def experience_reward(self) -> int:
        reward = super().experience_reward
        return reward + reward * 50 // 100

    def roll_gold_reward(self) -> int:
        reward = super().roll_gold_reward()
        return reward + reward * 50 // 100
