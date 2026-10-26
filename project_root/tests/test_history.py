import pytest

from app.calculation import Calculation
from app.exceptions import HistoryError
from app.history import AutoSaveObserver, History, HistoryObserver, LoggingObserver
from app.logger import Logger

HEADER = "operation,operand_a,operand_b,result,timestamp\n"


def make_calc(result=5.0):
    return Calculation("add", 2.0, 3.0, result)


def test_add_and_get_all():
    history = History()
    history.add(make_calc())
    assert len(history.get_all()) == 1


def test_max_size_removes_oldest():
    history = History(max_size=2)
    for number in [1, 2, 3]:
        history.add(make_calc(number))
    assert [c.result for c in history.get_all()] == [2, 3]


def test_clear():
    history = History()
    history.add(make_calc())
    history.clear()
    assert history.get_all() == []


def test_save_and_read_round_trip(tmp_path):
    file = str(tmp_path / "sub" / "h.csv")
    history = History()
    history.add(make_calc())
    history.save_to_csv(file)

    loaded = History().read_from_csv(file)
    assert len(loaded) == 1
    assert loaded[0].operation == "add"
    assert loaded[0].result == 5.0


def test_read_missing_file(tmp_path):
    with pytest.raises(HistoryError):
        History().read_from_csv(str(tmp_path / "nope.csv"))


def test_read_empty_file(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("")
    with pytest.raises(HistoryError):
        History().read_from_csv(str(file))


def test_read_missing_columns(tmp_path):
    file = tmp_path / "bad.csv"
    file.write_text("a,b\n1,2\n")
    with pytest.raises(HistoryError):
        History().read_from_csv(str(file))


def test_read_bad_number(tmp_path):
    file = tmp_path / "bad.csv"
    file.write_text(HEADER + "add,abc,3,5,time\n")
    with pytest.raises(HistoryError):
        History().read_from_csv(str(file))


def test_save_error(tmp_path):
    # A file where a folder should be, so saving must fail
    blocker = tmp_path / "blocker.txt"
    blocker.write_text("x")
    with pytest.raises(HistoryError):
        History().save_to_csv(str(blocker / "h.csv"))


def test_base_observer_must_be_overridden():
    with pytest.raises(NotImplementedError):
        HistoryObserver().update(make_calc())


def test_logging_observer_writes_to_log(tmp_path):
    log_file = tmp_path / "t.log"
    LoggingObserver(Logger(str(log_file))).update(make_calc())
    assert "operation=add" in log_file.read_text()


def test_autosave_observer_creates_csv(tmp_path):
    file = tmp_path / "auto.csv"
    history = History()
    history.add(make_calc())
    AutoSaveObserver(history, str(file)).update(make_calc())
    assert file.exists()