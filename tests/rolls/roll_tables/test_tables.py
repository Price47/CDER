# Just one test to briefly check all the default tables
from src.rolls.role_tables.battlefield_detriments import (
    BattleFieldDetriments,
    entries as battlefield_detriment_entries,
)
from src.rolls.role_tables.lingering_injuries import (
    LingeringInjuries,
    entries as lingering_injuries_entries,
)


def test_battlefield_detriments_table(mocker):
    mocker.patch("src.rolls.dice.randint", side_effect=[2])
    t = BattleFieldDetriments()
    outcome = t.roll_table()

    # for a roll of '2', assert the 2nd table entry is returned
    assert outcome == battlefield_detriment_entries[1]


def test_lingering_injuries_table(mocker):
    mocker.patch("src.rolls.dice.randint", side_effect=[2, 6])
    t = LingeringInjuries()
    outcome = t.roll_table()

    # Lingering effect rolls translated to the correct index
    expected_lingering_effect_index = (2+6-2-1)

    # for a roll of '2', assert the 2nd table entry is returned
    assert outcome == lingering_injuries_entries[expected_lingering_effect_index]
