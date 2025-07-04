from src.turn.turn_queue import TurnQueue, TurnQueueEntry
from src.turn.turn_runner import TurnRunner


def test_turn_runner_run(character_actor_and_party_factory):
    character_actors, parties = character_actor_and_party_factory()
    _queue = [TurnQueueEntry.from_character_actor(c) for c in character_actors]

    queue = TurnQueue(queue=_queue)
    TurnRunner(turn_queue=queue, parties=parties).run()
