from tests.defaults import character_json


def test_from_json_method(character_factory):
    c = character_factory()
    default_json = character_json()

    assert c.ac == default_json.get("ac")
    assert c.target_priority == default_json["config"]["behavior"]["target_priority"]


def test_character_initiative_caching(mocker, character_factory):
    mocker.patch("src.rolls.dice.randint", side_effect=[14, 12])
    # 20 dex should be +5 to initiative modifier
    c = character_factory(dexterity=20)
    # c = Character.from_json(_character_json(dexterity=20))

    assert c.initiative == 19
    # Cached initiative should not use the new roll of 12 (or roll at all)
    assert c.initiative == 19
