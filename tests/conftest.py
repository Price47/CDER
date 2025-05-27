import pytest

from src.characters import Character
from tests.defaults import character_json


@pytest.fixture()
def default_character():
    return Character.from_json(character_json())


@pytest.fixture()
def character_factory(default_character):
    def character_factory(**kwargs):
        c_json = character_json(**kwargs)
        return Character.from_json(c_json)

    return character_factory
