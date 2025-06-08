import dataclasses
from typing import List, Any


from src.characters.data_structs.character_min_heap import CharacterHeap
from src.characters.character import Character


@dataclasses.dataclass
class Party:
    """
    Collection of characters
    """

    characters: List[Character]
    character_heap: CharacterHeap = None

    def __init__(self, characters: List[Character]):
        self.character_heap = CharacterHeap(characters)

    @property
    def characters(self) -> List[Character]:
        return self.character_heap.heap

    @classmethod
    def build_party(cls, characters: List[Character]) -> "Party":
        party = cls(characters)
        for c in characters:
            c.party = party

        return party
