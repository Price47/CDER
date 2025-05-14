from src.character.character import Character

default_json = {
    "hp": 30,
    "config": {
        "ac": 18,
        "hit_modifier": 2,
        "morale": 1,
        "behavior": {
            "target_priority": "most_healthy",
        }
    }
}

def test_from_json_method():
    c = Character.from_json(default_json)

    assert c.ac == 18
    assert c.target_priority == "most_healthy"

def test_hit_misses(mocker):
    mocker.patch("src.roll.dice.randint", side_effect=[10])
    c = Character.from_json(default_json)
    hit_damage = c.hit(12)
    assert hit_damage == 0

def test_hit(mocker):
    mocker.patch("src.roll.dice.randint", side_effect=[14, 6, 6])
    c = Character.from_json(default_json)
    hit_damage = c.hit(12)
    assert hit_damage == 6

def test_critical_hit(mocker):
    mocker.patch("src.roll.dice.randint", side_effect=[20, 8, 6])
    c = Character.from_json(default_json)
    hit_damage = c.hit(12)
    assert hit_damage == 14

def test_critical_miss(mocker):
    mocker.patch("src.roll.dice.randint", side_effect=[1, 8, 6])
    c = Character.from_json(default_json)
    hit_damage = c.hit(0)
    assert hit_damage == 0