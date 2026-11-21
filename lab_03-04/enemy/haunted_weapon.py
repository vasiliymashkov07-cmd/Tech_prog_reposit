from ..combat.hit import Hit
from ..core.dice import Dice
from ..defense.damage import Damage
from ..item.weapon import Weapon
from .enemy import Enemy


# Оружие теперь может участвовать в бою как враг.
class HauntedWeapon(Enemy):
    def __init__(self, weapon: Weapon) -> None:
        self._weapon = weapon
        # Запас здоровья зависит от урона оружия.
        self._max_health = weapon.damage * 5
        self._health = self._max_health

    @property
    def code(self) -> str:
        return "haunted-weapon"

    @property
    def name(self) -> str:
        return "Одержимый " + self._weapon.name

    @property
    def health(self) -> int:
        return self._health

    @property
    def max_health(self) -> int:
        return self._max_health

    def is_alive(self) -> bool:
        return self._health > 0

    def roll_damage(self) -> Hit:
        # Удар рассчитывает само оружие.
        return self._weapon.roll_damage()

    def receive_hit(self, amount: int) -> Damage:
        damage = Damage(amount)
        self._health = max(0, self._health - damage.amount)
        return damage

    @property
    def experience_reward(self) -> int:
        # Опыт зависит от стоимости оружия.
        return self._weapon.price // 2

    def roll_gold_reward(self) -> int:
        return Dice().roll(self._weapon.price // 4, self._weapon.price // 2)
