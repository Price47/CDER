from src.turn.turn_queue import TurnQueue, TurnQueueEntry
from src.turn.turn_runner import TurnRunner


def _max_damage_critical_roll():
    return [
        # Critical roll + 2 scar table + dmg
        20,
        8,
        1,
        10,
        10,
    ]


def test_turn_runner_run(mocker, character_actor_and_party_factory):
    _initiative_rolls = [11, 13, 15, 17]
    mocker_side_effect = (
        _initiative_rolls
        +
        # event table roll
        [6]
        + _max_damage_critical_roll()
        + _max_damage_critical_roll()
        + _max_damage_critical_roll()
        +
        # event table roll
        [6]
        + _max_damage_critical_roll()
        + _max_damage_critical_roll()
    )

    mocker.patch("src.rolls.dice.randint", side_effect=mocker_side_effect)

    character_actors, parties = character_actor_and_party_factory()

    # Set queue
    _queue = sorted(
        [TurnQueueEntry.from_character_actor(c) for c in character_actors],
        key=lambda q: q.character.initiative,
    )
    queue = TurnQueue(queue=_queue)

    # Run turn runner
    TurnRunner(turn_queue=queue, parties=parties).run()

    # Check results in parties
    winning_party = parties[0]
    defeated_party = parties[1]

    for c in winning_party.characters:
        assert c.is_alive is True

    for c in defeated_party.characters:
        assert c.is_alive is False

    # Second character should have received a lingering injury.
    assert winning_party.characters[1].details.battle_scars == ["Minor Scar"]
