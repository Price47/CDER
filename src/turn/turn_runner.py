from typing import Dict

from pydantic import BaseModel

from src.characters.character import Character
from src.turn.turn_queue import TurnQueueEntry, TurnQueue


class BattleState(BaseModel):
    belligerents: Dict[Character] = {"NPC": [], "Players": []}


class TurnRunner(BaseModel):
    turn_queue: TurnQueue
    next_turn_queue: TurnQueue

    def _tick(self):
        entry: TurnQueueEntry = self.turn_queue.get()
        character = entry.character
        character.act()
        self.next_turn_queue.put(entry)

    def run(self):
        while not self.turn_queue.empty():
            entry = self.turn_queue.get()
            self.next_turn_queue.put(entry)

        print("turn over")
