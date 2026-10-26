import pytest

from app.exceptions import ValidationError
from app.input_validators import InputValidator


@pytest.mark.parametrize("value, expected", [
    ("5", 5.0), ("-2.5", -2.5), (3, 3.0), ("1000000", 1000000.0),
])
def test_valid_numbers(value, expected):
    assert InputValidator.validate_number(value, 1000000) == expected


@pytest.mark.parametrize("value", ["abc", "", "nan", "inf", None, "1000001"])
def test_invalid_numbers(value):
    with pytest.raises(ValidationError):
        InputValidator.validate_number(value, 1000000)