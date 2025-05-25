import pytest

from src.characters.character import CharacterStats
from src.rolls.attribute_rolls import (
    StrRoll,
    DexRoll,
    ConRoll,
    IntRoll,
    WisRoll,
    ChaRoll,
)


@pytest.mark.parametrize(
    "cls,expected_roll",
    [
        # Expected rolls based on the 10 side effect for randint in dice,
        # and the provided stats values in the test
        pytest.param(StrRoll, 10, id="str"),
        pytest.param(DexRoll, 11, id="dex"),
        pytest.param(ConRoll, 12, id="con"),
        pytest.param(IntRoll, 13, id="int"),
        pytest.param(WisRoll, 14, id="wis"),
        pytest.param(ChaRoll, 15, id="cha"),
    ],
)
def test_attribute_rolls_use_correct_attribute(mocker, cls, expected_roll):
    mocker.patch("src.rolls.dice.randint", side_effect=[10])
    stats = CharacterStats(
        strength=10,
        dexterity=12,
        constitution=14,
        intelligence=16,
        wisdom=18,
        charisma=20,
    )

    assert cls(stats=stats).roll() == expected_roll
