from dataclasses import field
from typing import List

from pydantic import BaseModel

from src.characters import Character


class TurnQueueEntry(BaseModel):
    # manually handle turn
    handle_turn_manually: bool = False
    character: Character

    @classmethod
    def from_character(cls, character: Character) -> "TurnQueueEntry":
        return cls(
            character=character,
            handle_turn_manually=character.handle_turn_manually,
        )


class TurnQueue(BaseModel):
    """
    Simple queue implementation for turns, but with the standard functions from the all python
    builtin queues https://docs.python.org/3/library/queue.html#queue.Queue. FIFO by nature
    so no handling for any other ordering, order characters are added to the queue is the order
    they'll pop out
    """

    queue: List[TurnQueueEntry] = field(default_factory=lambda: [])

    def qsize(self) -> int:
        return len(self.queue)

    def empty(self):
        return len(self.queue) == 0

    def put(self, entry: TurnQueueEntry):
        self.queue.append(entry)

    def get(self) -> TurnQueueEntry:
        return self.queue.pop(0)
