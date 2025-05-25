from typing import Dict

from pydantic import BaseModel

from src.characters.character import Character


class Battle(BaseModel):
    """
    Describe and configure a large scale battle
    """

    belligerents: Dict[Character] = {"NPC": [], "Players": []}
