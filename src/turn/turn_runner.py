from dataclasses import field
from pydantic import BaseModel
from typing import List

from src.characters import Character
from src.characters.party import Party
from src.context import current_round
from src.logger import event_logger as logger
from src.rolls.role_tables.battlefield_detriments import BattleFieldDetriments
from src.turn.turn_queue import TurnQueue, TurnQueueEntry
from tests.defaults import character_json


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

    def run_actions(self):
        while not self.turn_queue.empty():
            entry = self.turn_queue.get()
            entry.character.act()
            self.next_turn_queue.put(entry)

        self.turn_queue = self.next_turn_queue
        self.next_turn_queue = TurnQueue()

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
        self.run_actions()

    def run(self):
        for i in range(1, 500):
            current_round.set(i)
            self.run_round()


if __name__ == "__main__":
    party_one = Party.build_party(
        characters=[Character.from_json(character_json()) for i in range(100)]
    )
    party_two = Party.build_party(
        characters=[Character.from_json(character_json()) for i in range(100)]
    )

    _queue = [TurnQueueEntry.from_character(c) for c in party_one.characters] + [
        TurnQueueEntry.from_character(c) for c in party_two.characters
    ]

    queue = TurnQueue(queue=_queue)
    TurnRunner(turn_queue=queue).run()
