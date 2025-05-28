import enum
from typing import List, Any, Tuple

from pydantic import BaseModel

from src.rolls.dice import Die, D6, D12, D20, D8, D100, D4, D10


class RollTableValidationError(Exception):
    pass


class RollModel(enum.Enum):
    # Standard, pure chance rolls
    STANDARD = "standard"
    # Generate rolls chances closer to a mild bell curve, by using multiple die to make
    # the high and low extremes less likely. (The math on this as is is shakey and
    # questionable at best, but basically right). Returning the same table entry for multiple
    # rolls will also help bell-curve-ify, to make less extreme results more common
    BELL = "bell-curve"


class RollTable(BaseModel):
    """
    Model rep for a simple rolls table, for any given table that you can roll some DX for to
    generate random events
    """

    model: RollModel = RollModel.STANDARD
    dx: type[Die]
    dice: List[Die] = None
    table_entries: List[str]

    def _bell_model_die_combinations(self) -> Tuple[List[Die], int]:
        dx = self.dx()
        if isinstance(dx, D10):
            return [D4(), D6()], 9
        if isinstance(dx, D12):
            return [D6(), D6()], 11
        if isinstance(dx, D20):
            return [D8(), D12()], 19
        if isinstance(dx, D100):
            return [D20(), D20(), D20(), D20(), D20()], 95

        raise RollTableValidationError(
            "Bell model should only be used for a D10, D12, D20, or D100 table"
        )

    def model_post_init(self, _context: Any):
        if self.model == RollModel.STANDARD:
            expected_table_length = self.dx().die_max
            if len(self.table_entries) != expected_table_length:
                raise RollTableValidationError(
                    f"Table Length ({len(self.table_entries)} rows found) should match highest die "
                    f"value {expected_table_length}"
                )
            self.dice = [self.dx()]
        if self.model == RollModel.BELL:
            _dice, expected_table_length = self._bell_model_die_combinations()
            # With this model, the lowest possible value won't be 1, it'll be 2 or 5, so need
            # to adjust table length expectations accordingly
            if len(self.table_entries) != expected_table_length:
                raise RollTableValidationError(
                    f"Table Length ({len(self.table_entries)} rows found) should be {expected_table_length} "
                    f"for a {self.dx()} rolls table using bell curve rolls method (to account for minimum rolls NOT "
                    f"being 1"
                )

            self.dice = _dice

    def _roll(self):
        return sum([d.roll() for d in self.dice])

    def roll_table(self):
        _roll = self._roll()
        return self.table_entries[_roll - 1]
