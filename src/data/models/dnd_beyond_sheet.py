from typing import List

from pydantic import BaseModel

from src.rolls.dice_pool import DamageRoll, HitRoll
from src.shared_models.cased_model import DNDModel
from src.shared_models.character_stats import CharacterStats


class CharacterWeapon(BaseModel):
    name: str
    hit_die: HitRoll
    damage_die: DamageRoll


class CharacterWeapons(BaseModel):
    weapons: List[CharacterWeapon]

    @property
    def primary(self):
        return self.weapons[0]

    @classmethod
    def from_extracted_data(cls, weapons_data):
        weapons = []
        # Fetch 9 weapons max (shouldn't be more than like 3 realistically)
        for i in range(1, 10):
            # Weapon 1 name isn't numbered
            name = weapons_data.get(f"WpnName{i if i > 1 else ''}")

            if not name:
                break

            hit_modifier = weapons_data[f"Wpn{i}AtkBonus"]
            damage = weapons_data[f"Wpn{i}Damage"]
            damage_info = damage.split(" ")[0].split("+")
            if len(damage_info) != 2:
                # should be the case just for unarmed
                continue

            [xdx, damage_modifier] = damage_info
            damage_die = DamageRoll.from_string(xdx, damage_modifier)
            hit_die = HitRoll(modifier=hit_modifier)

            weapons.append(
                CharacterWeapon(name=name, damage_die=damage_die, hit_die=hit_die)
            )

        return cls(weapons=weapons)


class CharacterItem(BaseModel):
    name: str
    qty: int
    weight: str


class CharacterItems(BaseModel):
    items: List[CharacterItem]

    @classmethod
    def from_extracted_data(cls, items_data):
        items = []
        for i in range(10):
            if name := items_data.get(f"EqName{i}"):
                items.append(
                    CharacterItem(
                        name=name,
                        qty=items_data[f"EqQty{i}"],
                        weight=items_data[f"EqWeight{i}"],
                    )
                )
            else:
                break

        return cls(items=items)


class DNDBeyondExtractedCharacterData(DNDModel):
    character_name: str
    max_hp: int
    ac: int
    _str: int
    _int: int
    _dex: int
    _wis: int
    _con: int
    _cha: int
    speed: str
    weapons: CharacterWeapons = None
    items: CharacterItems = None

    @staticmethod
    def _filter_data(data: dict, key: str) -> dict:
        return {k: v for k, v in data.items() if key in k}

    def __init__(self, **data):
        super().__init__(**data)
        # Check for some values that could, but might not, exist, from which we can
        # derive some stats to assign to the character, like hit modifier based and dmg
        # on an equipped weapon
        self._int = data.get("INT")
        self._str = data.get("STR")
        self.weapons = CharacterWeapons.from_extracted_data(
            self._filter_data(data, "Wpn")
        )
        self.items = CharacterItems.from_extracted_data(self._filter_data(data, "Eq"))

    @property
    def stats(self) -> CharacterStats:
        return CharacterStats(
            strength=self._str,
            dexterity=self._dex,
            constitution=self._con,
            intelligence=self._int,
            charisma=self._cha,
            wisdom=self._wis,
        )

    @property
    def hit_modifier(self):
        return self.weapons.primary.hit_die.modifier

    def __str__(self):
        return f"Character Model for {self.character_name}"
