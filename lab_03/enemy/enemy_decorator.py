from ..combat.hit import Hit
from ..defense.damage import Damage
from .enemy import Enemy


class EnemyDecorator(Enemy):
    def __init__(self, wrapped: Enemy) -> None:
        self._wrapped = wrapped

    @property
    def code(self) -> str:
        return self._wrapped.code

    @property
    def name(self) -> str:
        return self._wrapped.name

    @property
    def health(self) -> int:
        return self._wrapped.health

    @property
    def max_health(self) -> int:
        return self._wrapped.max_health

    @property
    def experience_reward(self) -> int:
        return self._wrapped.experience_reward

    def is_alive(self) -> bool:
        return self._wrapped.is_alive()

    def roll_damage(self) -> Hit:
        return self._wrapped.roll_damage()

    def receive_hit(self, amount: int) -> Damage:
        return self._wrapped.receive_hit(amount)

    def roll_gold_reward(self) -> int:
        return self._wrapped.roll_gold_reward()
