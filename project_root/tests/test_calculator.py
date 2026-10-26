import pytest

from pathlib import Path

from app.calculator import Calculator, run_repl
from app.exceptions import HistoryError, OperationError, ValidationError


def test_calculate_returns_result(calc):
    calculation = calc.calculate("add", "2", "3")
    assert calculation.result == 5
    assert len(calc.get_history()) == 1


def test_result_is_rounded_to_precision(monkeypatch):
    monkeypatch.setenv("CALCULATOR_PRECISION", "2")
    assert Calculator().calculate("divide", "1", "3").result == 0.33


def test_invalid_number_raises(calc):
    with pytest.raises(ValidationError):
        calc.calculate("add", "abc", "1")


def test_unknown_operation_raises(calc):
    with pytest.raises(OperationError):
        calc.calculate("banana", "1", "2")


def test_divide_by_zero_raises_and_is_not_saved(calc):
    with pytest.raises(OperationError):
        calc.calculate("divide", "1", "0")
    assert calc.get_history() == []


def test_undo_and_redo(calc):
    calc.calculate("add", "1", "1")
    calc.calculate("add", "2", "2")
    calc.undo()
    assert len(calc.get_history()) == 1
    calc.redo()
    assert len(calc.get_history()) == 2


def test_undo_with_nothing_raises(calc):
    with pytest.raises(HistoryError):
        calc.undo()


def test_redo_with_nothing_raises(calc):
    with pytest.raises(HistoryError):
        calc.redo()


def test_new_calculation_clears_redo(calc):
    calc.calculate("add", "1", "1")
    calc.undo()
    calc.calculate("add", "2", "2")
    with pytest.raises(HistoryError):
        calc.redo()


def test_clear_history_can_be_undone(calc):
    calc.calculate("add", "1", "1")
    calc.clear_history()
    assert calc.get_history() == []
    calc.undo()
    assert len(calc.get_history()) == 1


def test_save_and_load_history(calc):
    calc.calculate("add", "2", "3")
    calc.save_history()
    calc.clear_history()
    calc.load_history()
    assert len(calc.get_history()) == 1
    assert calc.get_history()[0].result == 5


def test_load_missing_file_raises(calc):
    with pytest.raises(HistoryError):
        calc.load_history()


def test_autosave_creates_csv_file(calc):
    calc.calculate("add", "1", "2")
    assert Path(calc.config.history_file).exists()


def test_autosave_can_be_turned_off(monkeypatch):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    calc = Calculator()
    calc.calculate("add", "1", "2")
    assert not Path(calc.config.history_file).exists()


def test_max_history_size(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "2")
    calc = Calculator()
    for number in ["1", "2", "3"]:
        calc.calculate("add", number, "0")
    assert len(calc.get_history()) == 2


def test_calculation_is_written_to_log(calc):
    calc.calculate("multiply", "2", "3")
    assert "operation=multiply" in Path(calc.config.log_file).read_text()


def test_failing_observer_does_not_stop_calculator(tmp_path, monkeypatch):
    # Point the history folder at a file so the auto-save fails
    blocker = tmp_path / "blocker.txt"
    blocker.write_text("x")
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(blocker))
    calc = Calculator()
    calc.calculate("add", "1", "2")
    assert len(calc.get_history()) == 1
    assert "Observer failed" in Path(calc.config.log_file).read_text()


# ---------------- REPL tests ----------------

def type_commands(monkeypatch, commands):
    """Pretend the user typed these commands one after another."""
    answers = iter(commands)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))


def test_repl_normal_use(monkeypatch, capsys):
    type_commands(monkeypatch, [
        "help", "add 2 3", "multiply 4 5", "history", "undo", "redo",
        "save", "clear", "history", "load", "history", "exit",
    ])
    run_repl()
    output = capsys.readouterr().out
    assert "Available commands" in output
    assert "Result: 5.0" in output
    assert "Result: 20.0" in output
    assert "1. add(2.0, 3.0) = 5.0" in output
    assert "No calculations yet." in output
    assert "History loaded." in output
    assert "Goodbye!" in output


def test_repl_shows_friendly_errors(monkeypatch, capsys):
    type_commands(monkeypatch, [
        "", "bogus", "add 1", "divide 1 0", "add x 2",
        "undo", "redo", "load", "exit",
    ])
    run_repl()
    output = capsys.readouterr().out
    assert "Unknown command 'bogus'" in output
    assert "Usage: add" in output
    assert "Cannot divide by zero." in output
    assert "is not a valid number" in output
    assert "Nothing to undo." in output
    assert "Nothing to redo." in output
    assert "History file not found" in output


def test_repl_stops_on_end_of_input(monkeypatch, capsys):
    def raise_eof(prompt=""):
        raise EOFError

    monkeypatch.setattr("builtins.input", raise_eof)
    run_repl()
    assert "Goodbye!" in capsys.readouterr().out