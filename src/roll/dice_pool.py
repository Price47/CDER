from pydantic import BaseModel
from src.roll.dice import Die, D20


class RollXDX(BaseModel):
    x: int = 1
    dx: type[Die] = None

    @property
    def dice_pool(self):
        return [self.dx()] * self.x

    def roll(self, **kwargs):
        return sum([d.roll() for d in self.dice_pool])


class RollXDXPlusModifier(RollXDX):
    modifier: int = 0


class HitRoll(RollXDXPlusModifier):
    dx: type[Die] = D20
    critical_success: bool = False
    critical_failure: bool = False

    def roll(self):
        _roll = super().roll()
        self.critical_success = _roll == 20
        self.critical_failure = _roll == 1
        return _roll + self.modifier


class DamageRoll(RollXDXPlusModifier):
    def roll(self, **kwargs) -> int:
        if kwargs.get("critical"):
            # double rolled damage die
            self.x = self.x * 2

        return super().roll()
