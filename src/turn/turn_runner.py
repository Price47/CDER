from dataclasses import field
from pydantic import BaseModel
from typing import List

from src.characters.party import Party
from src.context import current_round
from src.logger import event_logger as logger
from src.rolls.role_tables.battlefield_detriments import BattleFieldDetriments
from src.runner.generate_actors import generate_actors
from src.turn.turn_queue import TurnQueue, TurnQueueEntry


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
    parties: List[Party]
    victors: Party = field(init=False, default=None)

    def _check_battle_over(self) -> bool:
        if sum([1 for p in self.parties if not p.is_wiped]) == 1:
            return True

        return False

    def run_actions(self):
        while not self.turn_queue.empty():
            entry = self.turn_queue.get()
            entry.act()

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

    def summarize(self):
        initial_combatants = sum([p.party_size for p in self.parties])
        logger.info(
            f"The battle is won. {initial_combatants} started, {len(self.victors.active_party_members)} remain"
        )
        for m in self.victors.active_party_members:
            print(m.id)
            print(m.details.battle_scars)

    def run(self):
        while not self._check_battle_over():
            _current_round = current_round.get()
            current_round.set(_current_round + 1)
            self.run_round()

        self.victors = list(filter(lambda p: not p.is_wiped, self.parties))[0]
        self.summarize()


if __name__ == "__main__":
    character_actors, parties = generate_actors()
    _queue = [TurnQueueEntry.from_character_actor(c) for c in character_actors]

    queue = TurnQueue(queue=_queue)
    TurnRunner(turn_queue=queue, parties=parties).run()
