import random
from typing import List

from pydantic import BaseModel, ConfigDict

from src.characters import Character
from src.characters.party import Party


class CharacterActor(BaseModel):
    character: Character
    party: Party
    opposing_parties: List[Party]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_target_party(self) -> Party:
        # TODO: Return min by attr by party
        return random.choice(self.opposing_parties)


def generate_character_actors_from_party(
    party: Party, opposing_parties: List[Party]
) -> List[CharacterActor]:
    return [
        CharacterActor(character=c, party=party, opposing_parties=opposing_parties)
        for c in party.characters
    ]
