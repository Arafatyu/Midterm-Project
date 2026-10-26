"""Loads settings from the .env file (or uses defaults)."""

import os

from dotenv import load_dotenv

from app.exceptions import ConfigError


def get_int(name, default):
    """Read a whole-number setting from the environment."""
    value = os.getenv(name, str(default))
    try:
        return int(value)
    except ValueError:
        raise ConfigError(f"{name} must be a whole number, but got '{value}'.")


def get_float(name, default):
    """Read a decimal-number setting from the environment."""
    value = os.getenv(name, str(default))
    try:
        return float(value)
    except ValueError:
        raise ConfigError(f"{name} must be a number, but got '{value}'.")


class CalculatorConfig:
    def __init__(self):
        load_dotenv()  # reads the .env file into environment variables

        # Folders and files (the second value in getenv is the default)
        self.log_dir = os.getenv("CALCULATOR_LOG_DIR", "logs")
        self.history_dir = os.getenv("CALCULATOR_HISTORY_DIR", "history")
        log_name = os.getenv("CALCULATOR_LOG_FILE", "calculator.log")
        history_name = os.getenv("CALCULATOR_HISTORY_FILE", "history.csv")
        self.log_file = os.path.join(self.log_dir, log_name)
        self.history_file = os.path.join(self.history_dir, history_name)

        # Other settings
        self.max_history_size = get_int("CALCULATOR_MAX_HISTORY_SIZE", 100)
        self.auto_save = os.getenv("CALCULATOR_AUTO_SAVE", "true").strip().lower() == "true"
        self.precision = get_int("CALCULATOR_PRECISION", 4)
        self.max_input_value = get_float("CALCULATOR_MAX_INPUT_VALUE", 1000000)
        self.encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

        self.validate()

    def validate(self):
        """Make sure the settings make sense."""
        if self.max_history_size < 1:
            raise ConfigError("CALCULATOR_MAX_HISTORY_SIZE must be at least 1.")
        if self.precision < 0:
            raise ConfigError("CALCULATOR_PRECISION cannot be negative.")
        if self.max_input_value <= 0:
            raise ConfigError("CALCULATOR_MAX_INPUT_VALUE must be greater than 0.")