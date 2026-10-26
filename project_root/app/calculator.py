"""The Calculator class (ties everything together) and the command-line REPL."""

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento, MementoCaretaker
from app.exceptions import CalculatorError, ValidationError
from app.history import AutoSaveObserver, History, LoggingObserver
from app.input_validators import InputValidator
from app.logger import Logger
from app.operations import OperationFactory


class Calculator:
    def __init__(self, config=None):
        self.config = config or CalculatorConfig()
        self.logger = Logger(self.config.log_file, self.config.encoding)
        self.history = History(self.config.max_history_size)
        self.caretaker = MementoCaretaker()

        # Observer pattern: register the observers
        self.observers = []
        self.add_observer(LoggingObserver(self.logger))
        if self.config.auto_save:
            self.add_observer(
                AutoSaveObserver(self.history, self.config.history_file, self.config.encoding)
            )

    def add_observer(self, observer):
        self.observers.append(observer)

    def _notify(self, calculation):
        """Tell every observer about the new calculation."""
        for observer in self.observers:
            try:
                observer.update(calculation)
            except CalculatorError as error:
                # An observer problem should not stop the calculator
                self.logger.error(f"Observer failed: {error}")

    def calculate(self, operation_name, first, second):
        """Validate the inputs, do the math, save to history, notify observers."""
        try:
            a = InputValidator.validate_number(first, self.config.max_input_value)
            b = InputValidator.validate_number(second, self.config.max_input_value)
            operation = OperationFactory.create(operation_name)
            result = round(operation.execute(a, b), self.config.precision)
        except ValidationError as error:
            self.logger.warning(f"Invalid input for {operation_name}: {error}")
            raise
        except CalculatorError as error:
            self.logger.error(f"{operation_name} {first} {second} failed: {error}")
            raise

        calculation = Calculation(operation_name.lower(), a, b, result)

        # Save a snapshot BEFORE changing the history, so undo can go back to it
        self.caretaker.save(CalculatorMemento(self.history.get_all()))
        self.history.add(calculation)
        self._notify(calculation)
        return calculation

    def get_history(self):
        return self.history.get_all()

    def clear_history(self):
        self.caretaker.save(CalculatorMemento(self.history.get_all()))
        self.history.clear()
        self.logger.info("History cleared.")

    def undo(self):
        memento = self.caretaker.undo(CalculatorMemento(self.history.get_all()))
        self.history.set_all(memento.calculations)
        self.logger.info("Undo performed.")

    def redo(self):
        memento = self.caretaker.redo(CalculatorMemento(self.history.get_all()))
        self.history.set_all(memento.calculations)
        self.logger.info("Redo performed.")

    def save_history(self):
        self.history.save_to_csv(self.config.history_file, self.config.encoding)
        self.logger.info("History saved.")

    def load_history(self):
        # Read first. If it fails, nothing has changed yet.
        loaded = self.history.read_from_csv(self.config.history_file, self.config.encoding)
        self.caretaker.save(CalculatorMemento(self.history.get_all()))
        self.history.set_all(loaded)
        self.logger.info("History loaded.")


# ---------------- Command-line interface (REPL) ----------------

HELP_TEXT = """Available commands:
  add, subtract, multiply, divide, power, root,
  modulus, int_divide, percent, abs_diff   (example: add 2 3)
  history   - show calculation history
  clear     - clear the history
  undo      - undo the last calculation
  redo      - redo the last undone calculation
  save      - save history to a CSV file
  load      - load history from a CSV file
  help      - show this message
  exit      - quit"""


def handle_command(calculator, command, args):
    """Run one command typed by the user."""
    if command in OperationFactory.available():
        if len(args) != 2:
            print(f"Usage: {command} <number1> <number2>")
            return
        calculation = calculator.calculate(command, args[0], args[1])
        print(f"Result: {calculation.result}")
    elif command == "history":
        calculations = calculator.get_history()
        if not calculations:
            print("No calculations yet.")
        for number, calculation in enumerate(calculations, start=1):
            print(f"{number}. {calculation}")
    elif command == "clear":
        calculator.clear_history()
        print("History cleared.")
    elif command == "undo":
        calculator.undo()
        print("Undo done.")
    elif command == "redo":
        calculator.redo()
        print("Redo done.")
    elif command == "save":
        calculator.save_history()
        print("History saved.")
    elif command == "load":
        calculator.load_history()
        print("History loaded.")
    elif command == "help":
        print(HELP_TEXT)
    else:
        print(f"Unknown command '{command}'. Type 'help' to see the commands.")


def run_repl():
    """Read-Eval-Print Loop: read a line, run it, print the result, repeat."""
    calculator = Calculator()
    print("Welcome to the calculator! Type 'help' for commands.")

    while True:
        try:
            line = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not line:
            continue  # ignore empty lines

        parts = line.split()
        command = parts[0].lower()
        args = parts[1:]

        if command == "exit":
            print("Goodbye!")
            break

        try:
            handle_command(calculator, command, args)
        except CalculatorError as error:
            print(f"Error: {error}")


if __name__ == "__main__":  # pragma: no cover
    run_repl()