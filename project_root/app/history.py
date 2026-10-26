"""Stores the calculation history, saves/loads it with pandas, and holds the observers."""

import os

import pandas as pd

from app.calculation import Calculation
from app.exceptions import HistoryError

# The CSV file columns
COLUMNS = ["operation", "operand_a", "operand_b", "result", "timestamp"]


class History:
    def __init__(self, max_size=100):
        self.max_size = max_size
        self.calculations = []

    def add(self, calculation):
        self.calculations.append(calculation)
        # If we have too many, remove the oldest one
        if len(self.calculations) > self.max_size:
            self.calculations.pop(0)

    def clear(self):
        self.calculations = []

    def get_all(self):
        return list(self.calculations)

    def set_all(self, calculations):
        self.calculations = list(calculations)

    def save_to_csv(self, filepath, encoding="utf-8"):
        """Turn the history into a pandas DataFrame and write it to a CSV file."""
        try:
            folder = os.path.dirname(filepath)
            if folder:
                os.makedirs(folder, exist_ok=True)
            rows = [calc.to_dict() for calc in self.calculations]
            table = pd.DataFrame(rows, columns=COLUMNS)
            table.to_csv(filepath, index=False, encoding=encoding)
        except (OSError, ValueError) as error:
            raise HistoryError(f"Could not save history: {error}")

    def read_from_csv(self, filepath, encoding="utf-8"):
        """Read a CSV file with pandas and return a list of Calculation objects."""
        if not os.path.exists(filepath):
            raise HistoryError(f"History file not found: {filepath}")

        try:
            table = pd.read_csv(filepath, encoding=encoding)
        except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError, OSError) as error:
            raise HistoryError(f"Could not read history file: {error}")

        # Make sure all the columns we need are there
        missing = [name for name in COLUMNS if name not in table.columns]
        if missing:
            raise HistoryError(f"History file is missing columns: {', '.join(missing)}")

        try:
            loaded = [Calculation.from_dict(row) for row in table.to_dict("records")]
        except (ValueError, TypeError) as error:
            raise HistoryError(f"History file has bad data: {error}")

        return loaded[-self.max_size:]


# ---------------- Observer pattern ----------------

class HistoryObserver:
    """Base class. Observers get told whenever a new calculation is made."""

    def update(self, calculation):
        raise NotImplementedError("Each observer must write its own update()")


class LoggingObserver(HistoryObserver):
    """Writes every calculation to the log file."""

    def __init__(self, logger):
        self.logger = logger

    def update(self, calculation):
        self.logger.info(
            f"Calculation: operation={calculation.operation}, "
            f"operands=({calculation.operand_a}, {calculation.operand_b}), "
            f"result={calculation.result}"
        )


class AutoSaveObserver(HistoryObserver):
    """Saves the whole history to the CSV file after every calculation."""

    def __init__(self, history, filepath, encoding="utf-8"):
        self.history = history
        self.filepath = filepath
        self.encoding = encoding

    def update(self, calculation):
        self.history.save_to_csv(self.filepath, self.encoding)