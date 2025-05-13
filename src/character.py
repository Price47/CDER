from typing import Literal, Union, Optional

from pydantic import BaseModel


class BehaviorConfig(BaseModel):
    target_priority: Optional[
        Union[Literal["strongest", "weakest", "most_healthy", "least_healthy"]]
    ] = "most_healthy"


class CharacterConfig(BaseModel):
    ac: int
    hit: int
    morale: int
    behavior: BehaviorConfig


class Character(BaseModel):
    health: int
    config: CharacterConfig

    @property
    def ac(self):
        return self.config.ac

    @property
    def target_priority(self):
        return self.config.behavior.target_priority

    @classmethod
    def from_json(cls, json):
        return cls(
            health=json["health"],
            config=CharacterConfig(
                **json["config"]
            ),
        )

