import pytest

from app.calculator import Calculator


@pytest.fixture(autouse=True)
def use_temp_folders(tmp_path, monkeypatch):
    """autouse=True means every test uses temporary folders for logs and history."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))


@pytest.fixture
def calc():
    """Gives a test a fresh Calculator."""
    return Calculator()