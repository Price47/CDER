from src.character.character import Character
from tests.character.utils import _character_json


def test_hit_misses(mocker):
    mocker.patch("src.roll.dice.randint", side_effect=[10])
    c = Character.from_json(_character_json())
    # target character
    tc = Character.from_json(_character_json(ac=12))

    hit_damage = c.hit(tc)
    assert hit_damage == 0
    assert tc.hp == 30

def test_hit(mocker):
    mocker.patch("src.roll.dice.randint", side_effect=[14, 6, 6])
    c = Character.from_json(_character_json())
    # target character
    tc = Character.from_json(_character_json(ac=12))
    hit_damage = c.hit(tc)
    assert hit_damage == 6
    assert tc.hp == 30-hit_damage

def test_critical_hit(mocker):
    mocker.patch("src.roll.dice.randint", side_effect=[20, 8, 6])
    c = Character.from_json(_character_json())
    # target character
    tc = Character.from_json(_character_json(ac=12))

    hit_damage = c.hit(tc)
    assert hit_damage == 14
    assert tc.hp == 30-hit_damage


def test_critical_miss(mocker):
    mocker.patch("src.roll.dice.randint", side_effect=[1, 8, 6])
    c = Character.from_json(_character_json())
    # target character
    tc = Character.from_json(_character_json(ac=12))

    hit_damage = c.hit(tc)
    assert hit_damage == 0
    assert tc.hp == 30
