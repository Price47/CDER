import logging


logging.getLogger().setLevel(logging.DEBUG)


class EventLogger(logging.Logger):
    def __init__(self, name, level=logging.DEBUG):
        super().__init__(name, level)
        self.extra_info = None

    def info(self, msg, *args, **kwargs):
        super().info(msg, *args, extra=self.extra_info, **kwargs)


event_log_formatter = logging.Formatter("[%(name)s] (Round 1) %(message)s")
event_log_handler = logging.StreamHandler()
event_log_handler.setLevel(logging.DEBUG)
event_log_handler.setFormatter(event_log_formatter)


event_logger = logging.getLogger("Event Logger")
event_logger.addHandler(event_log_handler)
