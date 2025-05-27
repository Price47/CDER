from dataclasses import field

from pydantic import BaseModel

from src.turn.turn_queue import TurnQueue


class TurnRunner(BaseModel):
    turn_queue: TurnQueue
    next_turn_queue: TurnQueue = field(init=False, default_factory=TurnQueue)

    def run_turn(self):
        while not self.turn_queue.empty():
            entry = self.turn_queue.get()
            self.next_turn_queue.put(entry)

        print("turn over")
