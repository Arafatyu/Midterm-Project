"""Custom errors so we can give friendly, specific messages."""


class CalculatorError(Exception):
    """Parent class for all calculator errors."""


class OperationError(CalculatorError):
    """Raised when a math operation is not possible (like dividing by zero)."""


class ValidationError(CalculatorError):
    """Raised when the user's input is not valid."""


class ConfigError(CalculatorError):
    """Raised when a setting in the .env file is wrong."""


class HistoryError(CalculatorError):
    """Raised for undo/redo problems and CSV save/load problems."""