from typing import List

from pydantic import BaseModel, ConfigDict

from src.characters import Character
from src.characters.party import Party


class CharacterActor(BaseModel):
    character: Character
    party: Party
    opposing_parties: List[Party]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_target(self):
        target = self.opposing_parties[0].character_heap.peek()

        for p in self.opposing_parties[1:]:
            t = p.character_heap.peek()
            if t.hp < target.hp:
                target = t


def generate_character_actors_from_party(
    party: Party, opposing_parties: List[Party]
) -> List[CharacterActor]:
    return [
        CharacterActor(character=c, party=party, opposing_parties=opposing_parties)
        for c in party.characters
    ]
