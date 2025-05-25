from functools import cached_property
from typing import Literal, Union, Optional

from pydantic import BaseModel

from src.rolls.dice import D10
from src.rolls.dice_pool import HitRoll, DamageRoll


class CharacterStats(BaseModel):
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    charisma: int
    wisdom: int

    @staticmethod
    def _modifier(v: int) -> int:
        return (v - 10) // 2

    @property
    def str_modifier(self) -> int:
        return self._modifier(self.strength)

    @property
    def dex_modifier(self):
        return self._modifier(self.dexterity)

    @property
    def con_modifier(self) -> int:
        return self._modifier(self.constitution)

    @property
    def int_modifier(self) -> int:
        return self._modifier(self.intelligence)

    @property
    def wis_modifier(self) -> int:
        return self._modifier(self.wisdom)

    @property
    def cha_modifier(self) -> int:
        return self._modifier(self.charisma)


class BehaviorConfig(BaseModel):
    target_priority: Optional[Union[Literal["most_healthy", "least_healthy"]]] = (
        "most_healthy"
    )


class CharacterConfig(BaseModel):
    ac: int
    hit_modifier: int
    morale: int
    behavior: BehaviorConfig
    stats: Optional[CharacterStats] = None


class Character(BaseModel):
    hp: int
    config: CharacterConfig

    # ========= properties ========= #
    # nested and derived properties  #
    # ============================== #
    @property
    def behavior(self) -> BehaviorConfig:
        return self.config.behavior

    @property
    def stats(self) -> CharacterStats:
        return self.config.stats

    @property
    def ac(self):
        return self.config.ac

    @property
    def hit_modifier(self):
        return self.config.hit_modifier

    @property
    def target_priority(self):
        return self.config.behavior.target_priority

    @cached_property
    def initiative(self):
        return

    # ========= Character Interactions ========= #
    # Character actions towards other characters #
    # ========================================== #
    def hit(self, target_character: "Character") -> int:
        hit = HitRoll(modifier=self.hit_modifier)
        hit_roll = hit.roll()

        # Miss on a crit fail regardless of modifiers and target AC
        if hit.critical_failure:
            return 0

        if hit_roll > target_character.ac:
            damage = DamageRoll(dx=D10).roll(critical=hit.critical_success)
            target_character.hp -= damage
            return damage

        return 0

    # ========= class methods ========= #
    # generate characters classes        #
    # ================================= #
    @classmethod
    def from_json(cls, json):
        return cls(
            hp=json["hp"],
            config=CharacterConfig(**json["config"]),
        )
