import pytest

from src.rolls.dice import D10
from src.rolls.role_tables.roll_table import (
    RollTable,
    RollModel,
    RollTableValidationError,
)


def test_roll_table_returns_table_value__standard():
    rt = RollTable(model=RollModel.STANDARD, dx=D10, table_entries=["entry"] * 10)

    assert rt.roll_table() == "entry"


def test_roll_table_validations__standard():
    with pytest.raises(RollTableValidationError) as exc:
        RollTable(model=RollModel.STANDARD, dx=D10, table_entries=["entry"] * 9)

    assert "Table Length (9 rows found) should match highest die value 10" in str(exc)


def test_roll_table_validations__bell():
    with pytest.raises(RollTableValidationError) as exc:
        RollTable(model=RollModel.BELL, dx=D10, table_entries=["entry"] * 10)

    assert (
        "Table Length (10 rows found) should be 9 for a [ D10 ] rolls table using bell curve rolls method (to account for minimum rolls NOT being 1'"
        in str(exc)
    )
