from dataclasses import field
from pydantic import BaseModel
from typing import List


from src.logger import event_logger as logger
from src.rolls.role_tables.battlefield_detriments import BattleFieldDetriments
from src.turn.turn_queue import TurnQueue


class TurnRunnerConfig(BaseModel):
    round_dynamic_events: List = field(
        default=[
            BattleFieldDetriments,
        ]
    )


class TurnRunner(BaseModel):
    config: TurnRunnerConfig = field(default_factory=TurnRunnerConfig)
    turn_queue: TurnQueue
    next_turn_queue: TurnQueue = field(init=False, default_factory=TurnQueue)

    def run_turn(self):
        while not self.turn_queue.empty():
            entry = self.turn_queue.get()
            self.next_turn_queue.put(entry)

    def run_events(self):
        dynamic_event_tables = self.config.round_dynamic_events
        for event_table in dynamic_event_tables:
            evt = event_table().roll_table()
            logger.info(evt)

    def run_round(self):
        """
        Run a single round of combat
        """
        logger.info("Round started")
        self.run_events()
        self.run_turn()


if __name__ == "__main__":
    queue = TurnQueue(queue=[])
    TurnRunner(turn_queue=queue).run_round()
