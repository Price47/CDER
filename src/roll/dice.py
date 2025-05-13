from typing import Optional

from pydantic import BaseModel
from random import randint


class Die(BaseModel):
    verbose: bool = True
    die_max: int
    last_role: Optional[int] = None

    def roll(self):
        _roll = randint(1, self.die_max)
        self.last_role = _roll

        if self.verbose:
            print(self)

        return _roll

    def __str__(self):
        return f"{self.__name__}: {self.last_role if self.last_role else 'unrolled'}"


class D4(Die):
    __name__ = "[ D4 ]"
    die_max: int = 4


class D6(Die):
    __name__ = "[ D6 ]"
    die_max: int = 6


class D8(Die):
    __name__ = "[ D8 ]"
    die_max: int = 8


class D10(Die):
    __name__ = "[ D10 ]"
    die_max: int = 10


class D12(Die):
    __name__ = "[ D12 ]"
    die_max: int = 12


class D20(Die):
    __name__ = "[ D20 ]"
    die_max: int = 20
    critical_roll: bool = False

    @property
    def critical(self) -> Optional[str]:
        if self.last_role == 1:
            return "Critical Failure"
        if self.last_role == 20:
            return "Critical Success"

        return None

    def roll(self):
        _roll = super().roll()
        if _roll == 20:
            self.critical_roll = True

        return _roll

    def __str__(self):
        _str = f"{self.__name__}: {self.last_role if self.last_role else 'unrolled'}"

        if crit_string := self.critical:
            _str += f" <{crit_string}>"

        return _str


class D100(Die):
    __name__ = "[ D100 ]"
    die_max: int = 100
