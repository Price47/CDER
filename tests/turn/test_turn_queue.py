from src.turn.turn_queue import TurnQueueEntry, TurnQueue


def test_turn_queue_entry_creation(character_actor_factory):
    c = character_actor_factory()
    entry = TurnQueueEntry.from_character_actor(c)
    print(entry)
    assert entry.character.id == c.character.id


def test_turn_queue_qsize(character_actor_factory):
    turn_queue_entries = [
        TurnQueueEntry.from_character_actor(character_actor_factory()) for _ in range(5)
    ]
    queue = TurnQueue(queue=turn_queue_entries)
    assert queue.qsize() == len(turn_queue_entries)


def test_turn_queue_empty(character_actor_factory):
    queue = TurnQueue()
    assert queue.empty() == True

    queue = TurnQueue(
        queue=[TurnQueueEntry.from_character_actor(character_actor_factory())]
    )
    assert queue.empty() == False


def test_turn_queue_put(character_actor_factory):
    queue = TurnQueue()
    assert queue.queue == []

    entry = TurnQueueEntry.from_character_actor(character_actor_factory())
    queue.put(entry)

    assert queue.queue == [entry]


def test_turn_queue_get(character_actor_factory):
    entry = TurnQueueEntry.from_character_actor(character_actor_factory())
    queue = TurnQueue(queue=[entry])

    retrieved_entry = queue.get()
    assert retrieved_entry == entry


def test_turn_queue(character_actor_factory):
    entries = [
        TurnQueueEntry.from_character_actor(character_actor_factory()) for _ in range(5)
    ]
    queue = TurnQueue(queue=entries)

    assert queue.qsize() == len(entries)
    queue.put(TurnQueueEntry.from_character_actor(character_actor_factory()))

    assert queue.qsize() == len(entries) + 1

    entry = queue.get()
    # Fifo queue, entry should be first element from entries and should be removed from queue
    assert entry == entries[0]
    assert queue.get() == entries[1]
    assert queue.get() == entries[2]
    # should be 3 entries left in the queue now
    assert queue.qsize() == 3
