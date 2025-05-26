from typing import List

from src.characters import Character


class TurnQueueEntry:
    # manually handle turn
    manual: bool = False
    character: Character


class TurnQueue:
    """
    Simple queue implementation for turns, but with the standard functions from the all python
    builtin queues https://docs.python.org/3/library/queue.html#queue.Queue. FIFO by nature
    so no handling for any other ordering, order characters are added to the queue is the order
    they'll pop out
    """

    queue: List[TurnQueueEntry]

    def qsize(self) -> int:
        return len(self.queue)

    def empty(self):
        return len(self.queue) == 0

    def put(self, entry: TurnQueueEntry):
        self.queue.append(entry)

    def get(self) -> TurnQueueEntry:
        return self.queue.pop(0)
