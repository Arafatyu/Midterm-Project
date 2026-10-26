import pytest

from app.exceptions import OperationError
from app.operations import Operation, OperationFactory


# Parameterized test: one test function runs once for each row below
@pytest.mark.parametrize("name, a, b, expected", [
    ("add", 2, 3, 5),
    ("add", -1, 1, 0),
    ("subtract", 5, 3, 2),
    ("multiply", 4, 3, 12),
    ("divide", 10, 4, 2.5),
    ("power", 2, 3, 8),
    ("power", 2, -1, 0.5),
    ("root", 27, 3, 3),
    ("root", 9, 2, 3),
    ("root", -8, 3, -2),
    ("modulus", 10, 3, 1),
    ("int_divide", 7, 2, 3),
    ("int_divide", -7, 2, -4),
    ("percent", 50, 200, 25),
    ("abs_diff", 3, 10, 7),
])
def test_operations_give_correct_result(name, a, b, expected):
    operation = OperationFactory.create(name)
    assert operation.execute(a, b) == pytest.approx(expected)


# Each row here should raise an OperationError
@pytest.mark.parametrize("name, a, b", [
    ("divide", 1, 0),
    ("power", 0, -1),
    ("power", -8, 0.5),
    ("power", 10.0, 10000.0),
    ("root", 4, 0),
    ("root", -4, 2),
    ("root", -8, 0.5),
    ("root", 0, -2),
    ("modulus", 5, 0),
    ("int_divide", 5, 0),
    ("percent", 5, 0),
])
def test_bad_operations_raise_error(name, a, b):
    operation = OperationFactory.create(name)
    with pytest.raises(OperationError):
        operation.execute(a, b)


def test_factory_is_not_case_sensitive():
    assert OperationFactory.create("ADD").execute(1, 2) == 3


def test_factory_unknown_operation():
    with pytest.raises(OperationError):
        OperationFactory.create("banana")


def test_factory_lists_all_ten_operations():
    assert len(OperationFactory.available()) == 10


def test_base_operation_must_be_overridden():
    with pytest.raises(NotImplementedError):
        Operation().execute(1, 2)