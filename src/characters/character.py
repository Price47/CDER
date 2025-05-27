from dataclasses import field
from uuid import uuid4, UUID
from functools import cached_property
from typing import Literal, Union, Optional, Any

from pydantic import BaseModel
from pydantic.v1 import UUID4

from src.rolls.attribute_rolls import DexRoll
from src.rolls.dice import D10
from src.rolls.dice_pool import HitRoll, DamageRoll
from src.shared_models.character_stats import CharacterStats


class BehaviorConfig(BaseModel):
    target_priority: Optional[Union[Literal["most_healthy", "least_healthy"]]] = (
        "most_healthy"
    )
    handle_turn_manually: bool = False


class CharacterConfig(BaseModel):
    hit_modifier: int
    morale: int
    behavior: BehaviorConfig
    stats: Optional[CharacterStats] = None


class Character(BaseModel):
    id: UUID = field(default=uuid4())
    ac: int
    hp: int
    max_hp: int = None
    config: CharacterConfig

    def model_post_init(self, context: Any):
        self.max_hp = self.hp

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
    def hit_modifier(self):
        return self.config.hit_modifier

    @property
    def target_priority(self):
        return self.config.behavior.target_priority

    @property
    def handle_turn_manually(self):
        return self.config.behavior.handle_turn_manually

    @cached_property
    def initiative(self):
        return DexRoll(stats=self.stats).roll()

    # ========= Character Interactions ========= #
    # Character actions towards other characters #
    # ========================================== #
    def roll_hit(self, target_character: "Character") -> int:
        hit = HitRoll(modifier=self.hit_modifier)
        hit_roll = hit.roll()

        # Miss on a crit fail regardless of modifiers and target AC
        if hit.critical_failure:
            return 0

        if hit_roll > target_character.ac:
            dmg = DamageRoll(dx=D10).roll(critical=hit.critical_success)
            target_character.take_damage(dmg)
            return dmg

        return 0

    def take_damage(self, dmg: int):
        self.hp -= dmg

    def heal(self, healing: int):
        health = self.hp + healing
        self.hp = min(health, self.max_hp)

    def act(self, target_character: "Character"):
        """
        Character action
        """
        self.roll_hit(target_character)

    # ========= class methods ========= #
    # generate characters classes        #
    # ================================= #
    @classmethod
    def from_json(cls, json):
        return cls(
            hp=json["hp"],
            ac=json["ac"],
            config=CharacterConfig(**json["config"]),
        )
