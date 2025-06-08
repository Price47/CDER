from typing import List, Tuple

from src.actors.character_actor import (
    generate_character_actors_from_party,
    CharacterActor,
)
from src.characters import Character
from src.characters.party import Party
from tests.defaults import character_json


def build_party() -> Party:
    return Party.build_party(
        characters=[Character.from_json(character_json()) for _ in range(10)]
    )


def build_parties() -> List[Party]:
    parties = [build_party() for _ in range(3)]
    return parties


def generate_actors() -> Tuple[List[CharacterActor], List[Party]]:
    parties = build_parties()
    actors = []

    for i in range(len(parties)):
        party = parties[i]
        opposing_parties = parties[:i] + parties[i + 1 :]
        actors.extend(generate_character_actors_from_party(party, opposing_parties))

    return sorted(
        actors, reverse=True, key=lambda actor: actor.character.initiative
    ), parties


if __name__ == "__main__":
    g, parties = generate_actors()
    for _g in g:
        print(_g.character.initiative)
