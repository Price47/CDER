from pydantic import BaseModel


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
