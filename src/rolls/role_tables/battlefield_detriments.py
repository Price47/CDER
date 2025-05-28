from src.rolls.dice import D6
from src.rolls.role_tables.roll_table import RollTable, RollModel

entries = [
    "Three cannonballs slam into the ground, spraying dirt and shaking the earth of three 15 ft. circles. Creatures "
    "in the affected areas must succeed a DC X Dexterity saving throw or be knocked prone. The areas are considered "
    "difficult terrain until the beginning of the next round.",
    "A trebuchet/scaffolding collapses nearby. Creatures in a 30 ft. line in the direction the structure falls in must "
    "succeed a DC X Dexterity saving throw or take 6d6 bludgeoning damage and be knocked prone. On a successful save, "
    "take half damage and are not knocked prone.",
    "The wind carries dust and debris in a thick cloud over the battlefield. The immediate area, out to a radius of 30 "
    "ft., is heavily obscured until the beginning of the next round.",
    "Spilled oil/gunpowder catches fire nearby, causing an explosion. Place the blast off to the side of the party’s "
    "current position. Creatures within 15 ft must make a DC X Constitution saving throw or be deafened until the "
    "beginning of the next round.",
    "A barrage of arrows flies toward the party in a 60 ft. cone. Creatures in the area must make a DC X Dexterity "
    "saving throw or take 4d6 piercing damage.",
    "No Effect",
]


class BattleFieldDetriments(RollTable):
    # Stolen from cottage of everything, with some additions
    # https://www.cottageofeverything.com/blog/world-weavers-guide-to-combat-large-scale-battles-in-5th-edition
    def __init__(self):
        super().__init__(dx=D6, table_entries=entries, model=RollModel.STANDARD)
