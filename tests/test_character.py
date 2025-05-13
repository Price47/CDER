from src.character import Character


def test_from_json_method():
    character_json = {
        "health": 30,
        "config": {
            "ac": 18,
            "hit": 2,
            "morale": 1,
            "behavior": {
                "target_priority": "strongest",
            }
        }
    }

    c = Character.from_json(character_json)

    assert c.ac == 18
    assert c.target_priority == "strongest"