"""All math operations, plus a Factory that creates them by name."""

from app.exceptions import OperationError


class Operation:
    """Base class. Every operation must have an execute(a, b) method."""

    def execute(self, a, b):
        raise NotImplementedError("Each operation must write its own execute()")


class Add(Operation):
    def execute(self, a, b):
        return a + b


class Subtract(Operation):
    def execute(self, a, b):
        return a - b


class Multiply(Operation):
    def execute(self, a, b):
        return a * b


class Divide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot divide by zero.")
        return a / b


class Power(Operation):
    def execute(self, a, b):
        # 0 to a negative power would be 1 / 0
        if a == 0 and b < 0:
            raise OperationError("Zero cannot be raised to a negative power.")
        try:
            result = a ** b
        except OverflowError:
            raise OperationError("The result is too large to calculate.")
        # Python gives a complex number for things like (-8) ** 0.5
        if isinstance(result, complex):
            raise OperationError("The result is not a real number.")
        return result


class Root(Operation):
    """Calculates the b-th root of a. Example: Root(27, 3) = 3."""

    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot take the 0th root.")
        if a < 0:
            # A negative number only has a real root if the root is odd
            if b != int(b) or int(b) % 2 == 0:
                raise OperationError("Cannot take an even root of a negative number.")
            return -Power().execute(-a, 1 / b)
        # The nth root is the same as raising to the power 1/n
        return Power().execute(a, 1 / b)


class Modulus(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot use modulus with zero.")
        return a % b


class IntDivide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot divide by zero.")
        return int(a // b)


class Percent(Operation):
    """Percentage(a, b) = (a / b) * 100"""

    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot calculate a percentage of zero.")
        return (a / b) * 100


class AbsDiff(Operation):
    def execute(self, a, b):
        return abs(a - b)


class OperationFactory:
    """Factory pattern: give it a name, get back the right operation object."""

    # Dictionary that connects a command name to its class
    _operations = {
        "add": Add,
        "subtract": Subtract,
        "multiply": Multiply,
        "divide": Divide,
        "power": Power,
        "root": Root,
        "modulus": Modulus,
        "int_divide": IntDivide,
        "percent": Percent,
        "abs_diff": AbsDiff,
    }

    @classmethod
    def create(cls, name):
        name = name.lower()
        if name not in cls._operations:
            raise OperationError(f"Unknown operation: '{name}'.")
        return cls._operations[name]()  # the () creates the object

    @classmethod
    def available(cls):
        return list(cls._operations)