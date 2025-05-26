from src.rolls.dice import D20, Die
from src.rolls.dice_pool import RollDX
from src.shared_models.character_stats import CharacterStats


class AttributeRoll(RollDX):
    dx: type[Die] = D20
    stats: CharacterStats


class StrRoll(AttributeRoll):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modifier = self.stats.str_modifier


class DexRoll(AttributeRoll):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modifier = self.stats.dex_modifier


class ConRoll(AttributeRoll):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modifier = self.stats.con_modifier


class IntRoll(AttributeRoll):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modifier = self.stats.int_modifier


class WisRoll(AttributeRoll):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modifier = self.stats.wis_modifier


class ChaRoll(AttributeRoll):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modifier = self.stats.cha_modifier
