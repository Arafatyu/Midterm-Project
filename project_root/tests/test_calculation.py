from app.calculation import Calculation


def test_calculation_stores_values():
    calc = Calculation("add", 2.0, 3.0, 5.0, "2026-01-01T10:00:00")
    assert calc.operation == "add"
    assert calc.operand_a == 2.0
    assert calc.operand_b == 3.0
    assert calc.result == 5.0
    assert calc.timestamp == "2026-01-01T10:00:00"


def test_timestamp_is_created_automatically():
    calc = Calculation("add", 1.0, 1.0, 2.0)
    assert calc.timestamp != ""


def test_to_dict_and_from_dict_round_trip():
    original = Calculation("multiply", 2.0, 4.0, 8.0, "2026-01-01T10:00:00")
    copy = Calculation.from_dict(original.to_dict())
    assert copy.to_dict() == original.to_dict()


def test_from_dict_converts_text_to_numbers():
    data = {"operation": "add", "operand_a": "2", "operand_b": "3",
            "result": "5", "timestamp": "t"}
    assert Calculation.from_dict(data).result == 5.0


def test_str_is_readable():
    calc = Calculation("add", 2.0, 3.0, 5.0)
    assert str(calc) == "add(2.0, 3.0) = 5.0"