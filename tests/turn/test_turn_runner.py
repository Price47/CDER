from src.turn.turn_queue import TurnQueue, TurnQueueEntry
from src.turn.turn_runner import TurnRunner


def test_turn_runner_run_round(character_actor_factory):
    entries = [
        TurnQueueEntry.from_character_actor(character_actor_factory())
        for _ in range(10)
    ]
    queue = TurnQueue(queue=entries)
    runner = TurnRunner(turn_queue=queue)

    for idx, e in enumerate(entries):
        assert e == runner.turn_queue.queue[idx]
    assert runner.next_turn_queue.queue == []

    runner.run_round()
    for idx, e in enumerate(entries):
        assert e == runner.turn_queue.queue[idx]
    assert runner.next_turn_queue.queue == []
