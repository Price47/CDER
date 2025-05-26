from src.characters.character import Character
from tests.characters.utils import _character_json


def test_from_json_method():
    c = Character.from_json(_character_json())

    assert c.ac == 18
    assert c.target_priority == "most_healthy"


def test_character_initiative_caching(mocker):
    mocker.patch("src.rolls.dice.randint", side_effect=[14, 12])
    # 20 dex should be +5 to initiative modifier
    c = Character.from_json(_character_json(dexterity=20))

    assert c.initiative == 19
    # Cached initiative should not use the new roll of 12 (or roll at all)
    assert c.initiative == 19
