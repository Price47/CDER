from src.rolls.dice import D20
from src.rolls.role_tables.roll_table import RollTable, RollModel

entries = (
    [
        "Lost an eye",
        "Lost a leg or foot",
    ]
    + ["Limp"] * 4
    + ["Minor Scar"] * 4
    + ["Broken Ribs"] * 2
    + ["Internal Injury"] * 2
    + ["Horrible Scar"] * 2
    + ["Festering Wound"] * 2
    + ["Lost an arm or hand"]
)


# https://www.dndbeyond.com/sources/dnd/dmg-2014/dungeon-masters-workshop#Injuries
class LingeringInjuries(RollTable):
    """
    Lingering injuries to apply to characters who takes critical damage
    """

    def __init__(self):
        super().__init__(dx=D20, table_entries=entries, model=RollModel.BELL)
