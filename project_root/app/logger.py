"""A small wrapper around Python's logging module."""

import logging
import os


class Logger:
    def __init__(self, log_file, encoding="utf-8"):
        # Make the log folder if it doesn't exist yet
        folder = os.path.dirname(log_file)
        if folder:
            os.makedirs(folder, exist_ok=True)

        self.logger = logging.getLogger("calculator")
        self.logger.setLevel(logging.INFO)

        # Remove old handlers so messages are not written twice
        for handler in list(self.logger.handlers):
            handler.close()
            self.logger.removeHandler(handler)

        # Send messages to the log file with a time and level
        file_handler = logging.FileHandler(log_file, encoding=encoding)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)