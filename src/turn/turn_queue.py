from dataclasses import field
from typing import List

from pydantic import BaseModel

from src.actors.character_actor import CharacterActor
from src.characters import Character


class TurnQueueEntry(BaseModel):
    # manually handle turn
    handle_turn_manually: bool = False
    character_actor: CharacterActor

    @property
    def initiative(self) -> int:
        return self.character.initiative

    @property
    def character(self) -> Character:
        return self.character_actor.character

    def act(self):
        target_party = self.character_actor.get_target_party()
        target_character = target_party.pop_target_character()

        if target_character:
            self.character.act(target_character)
            if target_character.hp > 0:
                target_party.character_heap.insert(target_character)

    @classmethod
    def from_character_actor(cls, character_actor: CharacterActor) -> "TurnQueueEntry":
        return cls(
            character_actor=character_actor,
            handle_turn_manually=character_actor.character.handle_turn_manually,
        )


class TurnQueue(BaseModel):
    """
    Simple queue implementation for turns, but with the standard functions from the all python
    builtin queues https://docs.python.org/3/library/queue.html#queue.Queue. FIFO by nature
    so no handling for any other ordering, order characters are added to the queue is the order
    they'll pop out
    """

    queue: List[TurnQueueEntry] = field(default_factory=lambda: [])

    # def model_post_init(self, queue: List[TurnQueueEntry] = None):
    #     self.queue = sorted(self.queue, key=lambda q: q.character.initiative, reverse=True)

    def qsize(self) -> int:
        return len(self.queue)

    def empty(self):
        return len(self.queue) == 0

    def put(self, entry: TurnQueueEntry):
        self.queue.append(entry)

    def get(self) -> TurnQueueEntry:
        return self.queue.pop(0)
