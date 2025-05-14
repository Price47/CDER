from dataclasses import field
from typing import List

from pydantic import BaseModel

from src.character.character import Character
from src.character.data_structs.character_min_heap import CharacterHeap


class Party(BaseModel):
    """
    Collection of characters
    """
    characters: List[Character]
    character_heap: CharacterHeap = field(init=False)

    def __post_init__(self):
        self.character_heap = CharacterHeap(self.characters)

