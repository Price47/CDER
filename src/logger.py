import logging

from src.context import current_round

logging.getLogger().setLevel(logging.DEBUG)

# Event Logger #
# Log different event actions, will include round number #


class RoundFilter(logging.Filter):
    def filter(self, record):
        record.round_number = current_round.get()
        return True


event_log_formatter = logging.Formatter(
    "[%(name)s] (Round %(round_number)d) %(message)s"
)
event_log_handler = logging.StreamHandler()
event_log_handler.setLevel(logging.DEBUG)
event_log_handler.setFormatter(event_log_formatter)


event_logger = logging.getLogger("Event Logger")
event_logger.addHandler(event_log_handler)
event_logger.addFilter(RoundFilter())
