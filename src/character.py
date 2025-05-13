from typing import Literal, Union, Optional

from pydantic import BaseModel

from src.roll.dice import D10
from src.roll.dice_pool import HitRoll, DamageRoll


class BehaviorConfig(BaseModel):
    target_priority: Optional[
        Union[Literal["strongest", "weakest", "most_healthy", "least_healthy"]]
    ] = "most_healthy"


class CharacterConfig(BaseModel):
    ac: int
    hit_modifier: int
    morale: int
    behavior: BehaviorConfig


class Character(BaseModel):
    health: int
    config: CharacterConfig

    # ========= properties ========= #
    # nested and derived properties  #
    # ============================== #
    @property
    def ac(self):
        return self.config.ac

    @property
    def hit_modifier(self):
        return self.config.hit_modifier

    @property
    def target_priority(self):
        return self.config.behavior.target_priority


    def hit(self, target_ac: int) -> int:
        hit = HitRoll(modifier=self.hit_modifier)
        hit_roll = hit.roll()

        # Miss on a crit fail regardless of modifiers and target AC
        if hit.critical_failure:
            return 0

        if hit_roll > target_ac:
            return DamageRoll(dx=D10).roll(critical=hit.critical_success)

        return 0

    # ========= class methods ========= #
    # generate character classes        #
    # ================================= #
    @classmethod
    def from_json(cls, json):
        return cls(
            health=json["health"],
            config=CharacterConfig(
                **json["config"]
            ),
        )

