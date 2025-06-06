from typing import List

from pydantic import BaseModel

from src.characters import Character
from src.characters.party import Party


class CharacterActor(BaseModel):
    character: Character
    party: Party
    opposing_parties: List[Party]

    def get_target(self):
        target = self.opposing_parties[0].character_heap.peek()

        for p in self.opposing_parties[1:]:
            t = p.character_heap.peek()
            if t.hp < target.hp:
                target = t
