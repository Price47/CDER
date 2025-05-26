def _character_json(**kwargs):
    return {
        "hp": kwargs.get("hp", 30),
        "ac": kwargs.get("ac", 18),
        "config": {
            "hit_modifier": kwargs.get("hit_modifier", 2),
            "morale": kwargs.get("morale", 1),
            "behavior": {
                "target_priority": kwargs.get("target_priority", "most_healthy"),
            },
            "stats": {
                "strength": kwargs.get("strength", 0),
                "dexterity": kwargs.get("dexterity", 0),
                "constitution": kwargs.get("constitution", 0),
                "intelligence": kwargs.get("intelligence", 0),
                "wisdom": kwargs.get("wisdom", 0),
                "charisma": kwargs.get("charisma", 0),
            },
        },
    }
