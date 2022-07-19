import os
import logging
from logging import handlers

LOG_FILENAME = "../log/siem_integration.log"


class Logger:
    def __init__(self, log_name, level="INFO"):
        if not os.path.isdir("../log/"):
            os.mkdir("../log/")
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(module)s - %(levelname)s - %(message)s"
        )
        handler = logging.handlers.RotatingFileHandler(
            LOG_FILENAME, maxBytes=200000000, backupCount=5
        )
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
