from typing import Any

from pydantic import BaseModel
from src.rolls.dice import Die, D20


class RollDX(BaseModel):
    dx: type[Die] = None
    die: Die = None
    modifier: int = 0

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
        return sum([d.roll() for d in self.dice_pool])


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
    def roll(self, **kwargs) -> int:
        if kwargs.get("critical"):
            # double rolled damage die, and regenerate dice pool
            self.x = self.x * 2
            self.generate_pool()

        return super().roll() + self.modifier
