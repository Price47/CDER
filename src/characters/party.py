import dataclasses
from functools import cached_property
from typing import List

from pydantic import ConfigDict

from src.characters.data_structs.character_min_heap import CharacterHeap
from src.characters.character import Character


@dataclasses.dataclass
class Party:
    """
    Collection of characters
    """

    characters: List[Character]
    character_heap: CharacterHeap = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __post_init__(self):
        self.character_heap = CharacterHeap(self.characters)

    @property
    def active_party_members(self) -> List[Character]:
        return list(filter(lambda c: c.is_alive, self.characters))

    @cached_property
    def party_size(self) -> int:
        return len(self.characters)

    @property
    def is_wiped(self):
        return len(self.active_party_members) == 0

    def check_target_character(self) -> Character:
        return self.character_heap.peek()

    def pop_target_character(self) -> Character:
        return self.character_heap.pop()

    @classmethod
    def build_party(cls, characters: List[Character]) -> "Party":
        party = cls(characters)
        for c in characters:
            c.party = party

        return party

