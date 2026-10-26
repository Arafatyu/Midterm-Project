"""A Calculation is one finished math problem saved in the history."""

from datetime import datetime


class Calculation:
    def __init__(self, operation, operand_a, operand_b, result, timestamp=None):
        self.operation = operation
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.result = result
        # If no time is given, use the current time
        self.timestamp = timestamp or datetime.now().isoformat(timespec="seconds")

    def to_dict(self):
        """Turn the calculation into a dictionary (used for the CSV file)."""
        return {
            "operation": self.operation,
            "operand_a": self.operand_a,
            "operand_b": self.operand_b,
            "result": self.result,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a Calculation from a dictionary (used when loading a CSV)."""
        return cls(
            str(data["operation"]),
            float(data["operand_a"]),
            float(data["operand_b"]),
            float(data["result"]),
            str(data["timestamp"]),
        )

    def __str__(self):
        return f"{self.operation}({self.operand_a}, {self.operand_b}) = {self.result}"