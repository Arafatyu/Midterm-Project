import pytest

from app.calculator_memento import CalculatorMemento, MementoCaretaker
from app.exceptions import HistoryError


def test_memento_keeps_a_copy():
    items = [1, 2]
    memento = CalculatorMemento(items)
    items.append(3)
    assert memento.calculations == [1, 2]


def test_undo_and_redo():
    caretaker = MementoCaretaker()
    caretaker.save(CalculatorMemento(["old"]))

    previous = caretaker.undo(CalculatorMemento(["new"]))
    assert previous.calculations == ["old"]

    again = caretaker.redo(CalculatorMemento(["old"]))
    assert again.calculations == ["new"]


def test_nothing_to_undo():
    with pytest.raises(HistoryError):
        MementoCaretaker().undo(CalculatorMemento([]))


def test_nothing_to_redo():
    with pytest.raises(HistoryError):
        MementoCaretaker().redo(CalculatorMemento([]))


def test_saving_clears_redo_stack():
    caretaker = MementoCaretaker()
    caretaker.save(CalculatorMemento([]))
    caretaker.undo(CalculatorMemento(["x"]))
    caretaker.save(CalculatorMemento([]))
    assert caretaker.redo_stack == []