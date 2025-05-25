# Just one test to briefly check all the default tables
from src.rolls.role_tables.battlefield_detriments import (
    BattleFieldDetriments,
    entries as battlefield_detriment_entries,
)


def test_battlefield_detriments_table(mocker):
    mocker.patch("src.rolls.dice.randint", side_effect=[2])
    t = BattleFieldDetriments()
    outcome = t.roll_table()

    # for a roll of '2', assert the 2nd table entry is returned
    assert outcome == battlefield_detriment_entries[1]
