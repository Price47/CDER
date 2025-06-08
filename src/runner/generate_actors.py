from typing import List

from src.actors.character_actor import generate_character_actors_from_party
from src.characters import Character
from src.characters.party import Party
from tests.defaults import character_json


def build_party() -> Party:
    return Party.build_party(
        characters=[Character.from_json(character_json()) for i in range(100)]
    )


def build_parties() -> List[Party]:
    parties = [build_party() for _ in range(3)]


def generate_actors():
    parties = build_parties()
    actors = []

    for i in range(len(parties)):
        party = parties[i]
        opposing_parties = parties[:i] + parties[i + 1 :]
        actors.append(generate_character_actors_from_party(party, opposing_parties))


if __name__ == "__main__":
    generate_actors()
