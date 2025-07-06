from typing import Tuple, List

import pytest

from src.actors.character_actor import (
    CharacterActor,
    generate_character_actors_from_party,
)
from src.characters import Character
from src.characters.party import Party
from tests.defaults import character_json


@pytest.fixture()
def default_character():
    return Character.from_json(character_json())


@pytest.fixture()
def character_factory():
    def character_factory(**kwargs):
        c_json = character_json(**kwargs)
        return Character.from_json(c_json)

    return character_factory


@pytest.fixture()
def character_actor_factory():
    def _character_factory(**kwargs):
        c_json = character_json(**kwargs)
        character = Character.from_json(c_json)
        p = Party([character])
        character.party = p

        opposing_character = Character.from_json(character_json(**kwargs))
        opposing_party = Party([opposing_character])

        character_actor = CharacterActor(
            character=character, party=p, opposing_parties=[opposing_party]
        )

        return character_actor

    return _character_factory


@pytest.fixture()
def character_actor_and_party_factory():
    def _character_actor_and_party_factory(
        *, party_count=2, characters_per_party=2
    ) -> Tuple[List[CharacterActor], List[Party]]:
        parties = []
        characters = []

        for _ in range(party_count):
            party = Party.build_party(
                characters=[
                    Character.from_json(character_json())
                    for _ in range(characters_per_party)
                ]
            )
            parties.append(party)

        for i in range(len(parties)):
            party = parties[i]
            opposing_parties = parties[:i] + parties[i + 1 :]
            characters.extend(
                generate_character_actors_from_party(party, opposing_parties)
            )

        return characters, parties

    return _character_actor_and_party_factory
