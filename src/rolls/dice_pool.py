from typing import Any

from pydantic import BaseModel
from src.rolls.dice import Die, D20, D8, D10, D12, D100, D4, D6


class RollDX(BaseModel):
    dx: type[Die] = None
    die: Die = None
    modifier: int = 0
    roll_value: int = None

    def model_post_init(self, _context: Any):
        self.die = self.dx()

    def roll(self, **kwargs):
        return self.die.roll() + self.modifier


class RollXDX(RollDX):
    """
    Roll XDX dice (2d4, 4d10, etc)
    """

    x: int = 1
    dice_pool: list[Die] = []

    def generate_pool(self):
        self.dice_pool = [self.dx()] * self.x

    def model_post_init(self, context: Any):
        self.generate_pool()

    def increase_pool(self, x):
        self.dice_pool.extend([self.dx()] * x)

    def roll(self, **kwargs):
        self.roll_value = sum([d.roll() for d in self.dice_pool])
        return self.roll_value

    @staticmethod
    def dx_die(dx_string: str) -> type[Die]:
        return {
            "4": D4,
            "6": D6,
            "8": D8,
            "10": D10,
            "12": D12,
            "20": D20,
            "100": D100,
        }[dx_string]

    @classmethod
    def from_string(cls, string: str, modifier: int = 0):
        """
        From the standard xdx format
        """

        x, dx = string.split("d")
        return cls(
            x=int(x),
            dx=cls.dx_die(dx),
            modifier=modifier,
        )


class CriticalRoll(RollXDX):
    """
    Model for any rolls that allows for critical success or failure
    """

    critical_success: bool = False
    critical_failure: bool = False

    def roll(self):
        _roll = super().roll()
        self.critical_success = _roll == 20
        self.critical_failure = _roll == 1
        return _roll + self.modifier


class HitRoll(CriticalRoll):
    dx: type[Die] = D20


class DamageRoll(RollXDX):
    damage_type: str = None

    def roll(self, **kwargs) -> int:
        if kwargs.get("critical"):
            # double rolled damage die, and regenerate dice pool
            self.x = self.x * 2
            self.generate_pool()

        return super().roll() + self.modifier
