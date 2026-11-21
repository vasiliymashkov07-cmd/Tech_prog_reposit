from enum import Enum


class EventType(Enum):
    HIT = "hit"
    CRITICAL_HIT = "critical_hit"
    DEATH = "death"
    POWER_STRIKE = "power-strike"
    DEFEND = "defend"
    EVADE = "evade"
    ABSORB = "absorb"
