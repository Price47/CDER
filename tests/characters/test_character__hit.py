from src.rolls.role_tables.lingering_injuries import (
    entries as lingering_injuries_entries,
)


def test_hit_misses(mocker, default_character, character_factory):
    mocker.patch("src.rolls.dice.randint", side_effect=[10])
    # target characters
    tc = character_factory(ac=12)

    hit_damage = default_character.roll_hit(tc)
    assert hit_damage == 0
    assert tc.hp == 30


def test_hit(mocker, default_character, character_factory):
    mocker.patch("src.rolls.dice.randint", side_effect=[14, 6, 6])
    # target characters
    tc = character_factory(ac=12)
    hit_damage = default_character.roll_hit(tc)
    assert hit_damage == 6
    assert tc.hp == 30 - hit_damage


def test_critical_hit(mocker, default_character, character_factory):
    mocker.patch(
        "src.rolls.dice.randint",
        side_effect=[
            # crit mock
            20,
            # 2 rolls for the lingering effects table
            5,
            10,
            # damage rolls
            8,
            6,
        ],
    )
    # Lingering effect rolls translated to the correct index
    expected_lingering_effect_index = 5 + 10 - 2 - 1
    # target characters
    tc = character_factory(ac=12)

    hit_damage = default_character.roll_hit(tc)
    assert hit_damage == 14
    assert tc.hp == 30 - hit_damage
    assert tc.details.battle_scars == [
        lingering_injuries_entries[expected_lingering_effect_index]
    ]


def test_critical_miss(mocker, default_character, character_factory):
    mocker.patch("src.rolls.dice.randint", side_effect=[1, 8, 6])
    # target characters
    tc = character_factory(ac=12)

    hit_damage = default_character.roll_hit(tc)
    assert hit_damage == 0
    assert tc.hp == 30
