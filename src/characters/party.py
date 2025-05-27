from typing import List, Any

from pydantic import BaseModel

from src.characters.character import Character
from src.characters.data_structs.character_min_heap import CharacterHeap


class Party(BaseModel):
    """
    Collection of characters
    """

    characters: List[Character]
    character_heap: CharacterHeap = None

    def model_post_init(self, _context: Any):
        self.character_heap = CharacterHeap(self.characters)
