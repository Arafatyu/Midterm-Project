"""Memento pattern: save snapshots of the history so we can undo and redo."""

from app.exceptions import HistoryError


class CalculatorMemento:
    """A snapshot (saved copy) of the history at one moment."""

    def __init__(self, calculations):
        self.calculations = list(calculations)  # list() makes a copy


class MementoCaretaker:
    """Keeps the undo and redo stacks of snapshots."""

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def save(self, memento):
        """Call this BEFORE the history changes."""
        self.undo_stack.append(memento)
        self.redo_stack.clear()  # a new change wipes out the redo steps

    def undo(self, current_memento):
        """Give back the previous snapshot, and keep the current one for redo."""
        if not self.undo_stack:
            raise HistoryError("Nothing to undo.")
        self.redo_stack.append(current_memento)
        return self.undo_stack.pop()

    def redo(self, current_memento):
        """Give back the snapshot we undid, and keep the current one for undo."""
        if not self.redo_stack:
            raise HistoryError("Nothing to redo.")
        self.undo_stack.append(current_memento)
        return self.redo_stack.pop()