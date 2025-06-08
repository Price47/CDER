import pytest

from src.actors.character_actor import CharacterActor
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
    def character_factory(**kwargs):
        c_json = character_json(**kwargs)
        character = Character.from_json(c_json)
        p = Party([character])
        character.party = p

        character_actor = CharacterActor(
            character=character, party=p, opposing_parties=[]
        )

        return character_actor

    return character_factory
