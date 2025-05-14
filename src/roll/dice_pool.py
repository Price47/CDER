from pydantic import BaseModel
from src.roll.dice import Die, D20


class RollXDX(BaseModel):
    """
    Roll XDX dice (2d4, 4d10, etc)
    """
    x: int = 1
    dx: type[Die] = None

    @property
    def dice_pool(self):
        return [self.dx()] * self.x

    def roll(self, **kwargs):
        return sum([d.roll() for d in self.dice_pool])


class RollXDXPlusModifierMixin(BaseModel):
    """
    Model mixin adding a modifier
    """
    modifier: int = 0


class CriticalRoll(RollXDX):
    """
    Model for any roll that allows for critical success or failure
    """
    critical_success: bool = False
    critical_failure: bool = False

    def roll(self):
        _roll = super().roll()
        self.critical_success = _roll == 20
        self.critical_failure = _roll == 1
        return _roll + self.modifier


class HitRoll(CriticalRoll, RollXDXPlusModifierMixin):
    dx: type[Die] = D20


class DamageRoll(RollXDX, RollXDXPlusModifierMixin):
    def roll(self, **kwargs) -> int:
        if kwargs.get("critical"):
            # double rolled damage die
            self.x = self.x * 2

        return super().roll()
