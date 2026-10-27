import os

import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigError

ALL_VARS = [
    "CALCULATOR_LOG_DIR", "CALCULATOR_LOG_FILE", "CALCULATOR_HISTORY_DIR",
    "CALCULATOR_HISTORY_FILE", "CALCULATOR_MAX_HISTORY_SIZE", "CALCULATOR_AUTO_SAVE",
    "CALCULATOR_PRECISION", "CALCULATOR_MAX_INPUT_VALUE", "CALCULATOR_DEFAULT_ENCODING",
]


def test_default_values(monkeypatch):
    # Stop it from reading the real .env file, and remove all settings
    monkeypatch.setattr("app.calculator_config.load_dotenv", lambda: None)
    for name in ALL_VARS:
        monkeypatch.delenv(name, raising=False)

    config = CalculatorConfig()
    assert config.log_file == os.path.join("logs", "calculator.log")
    assert config.history_file == os.path.join("history", "history.csv")
    assert config.max_history_size == 100
    assert config.auto_save is True
    assert config.precision == 4
    assert config.max_input_value == 1000000
    assert config.encoding == "utf-8"


def test_custom_values(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "5")
    monkeypatch.setenv("CALCULATOR_PRECISION", "2")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "50.5")
    config = CalculatorConfig()
    assert config.max_history_size == 5
    assert config.precision == 2
    assert config.auto_save is False
    assert config.max_input_value == 50.5


@pytest.mark.parametrize("name, value", [
    ("CALCULATOR_MAX_HISTORY_SIZE", "0"),
    ("CALCULATOR_PRECISION", "-1"),
    ("CALCULATOR_MAX_INPUT_VALUE", "0"),
    ("CALCULATOR_PRECISION", "abc"),
    ("CALCULATOR_MAX_INPUT_VALUE", "abc"),
])
def test_bad_settings_raise_config_error(monkeypatch, name, value):
    monkeypatch.setenv(name, value)
    with pytest.raises(ConfigError):
        CalculatorConfig()