from dataclasses import field
from uuid import uuid4, UUID
from functools import cached_property
from typing import Literal, Union, Optional, Any, List

from pydantic import BaseModel

from src.data.models.dnd_beyond_sheet import DNDBeyondExtractedCharacterData
from src.rolls.attribute_rolls import DexRoll
from src.rolls.dice import D10
from src.rolls.dice_pool import HitRoll, DamageRoll
from src.rolls.role_tables.lingering_injuries import LingeringInjuries
from src.shared_models.character_stats import CharacterStats


class BehaviorConfig(BaseModel):
    target_priority: Optional[Union[Literal["most_healthy", "least_healthy"]]] = (
        "most_healthy"
    )
    handle_turn_manually: bool = False


class CharacterConfig(BaseModel):
    hit_modifier: int
    morale: int = 0
    behavior: BehaviorConfig = field(default_factory=BehaviorConfig)
    stats: Optional[CharacterStats] = None


class CharacterDetails(BaseModel):
    battle_scars: List = field(default=[])

    def add_battle_scar(self):
        injury = LingeringInjuries().roll_table()
        self.battle_scars.append(injury)


class Character(BaseModel):
    id: UUID = field(default_factory=uuid4)
    ac: int
    hp: int
    max_hp: int = None
    config: CharacterConfig
    details: CharacterDetails = field(default_factory=CharacterDetails)
    party: Any = None

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

    @property
    def threat(self):
        return self.hp + self.ac

    # ========= Character Interactions ========= #
    # Character actions towards other characters #
    # ========================================== #
    def roll_hit(self, target_character: "Character") -> int:
        hit = HitRoll(modifier=self.hit_modifier)
        hit.roll()

        # Miss on a crit fail regardless of modifiers and target AC
        if hit.critical_failure:
            return 0

        return target_character.handle_hit_roll(hit)

    def handle_hit_roll(self, hit_roll: HitRoll):
        if hit_roll.roll_value < self.ac:
            return 0

        if hit_roll.critical_success:
            self.details.add_battle_scar()

        dmg = DamageRoll(dx=D10).roll(critical=hit_roll.critical_success)
        self.hp -= dmg

        return dmg

    def heal(self, healing: int):
        health = self.hp + healing
        self.hp = min(health, self.max_hp)

    def act(self, target_character: "Character" = None):
        """
        Character action
        """
        print(f"target character BEFORE action {target_character}")
        self.roll_hit(target_character)
        print(f"target character AFTER action {target_character}")



    # def __str__(self):
    #     return f"Character {self.id}"

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

    @classmethod
    def from_extracted_dnd_beyond_data(cls, data: DNDBeyondExtractedCharacterData):
        config = CharacterConfig(hit_modifier=data.hit_modifier, stats=data.stats)

        return cls(hp=data.max_hp, ac=data.ac, config=config)
