from pydantic import BaseModel
from src.roll.dice import Die

class RollXDX(BaseModel):
    x: int
    dx: type[Die]

    @property
    def dice_pool(self):
        return [self.dx()] * self.x

    def roll(self):
        return sum([d.roll() for d in self.dice_pool])

class DamageRoll(RollXDX):
    modifier: int

    def roll(self):
        return super().role() + self.modifier