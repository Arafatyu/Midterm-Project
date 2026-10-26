"""Checks that what the user typed is a usable number."""

import math

from app.exceptions import ValidationError


class InputValidator:
    @staticmethod
    def validate_number(value, max_value):
        """Turn the input into a float, or raise ValidationError."""
        try:
            number = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"'{value}' is not a valid number.")

        # float("nan") and float("inf") work in Python, but we don't want them
        if math.isnan(number) or math.isinf(number):
            raise ValidationError(f"'{value}' is not a valid number.")

        if abs(number) > max_value:
            raise ValidationError(f"{value} is too big. The maximum allowed is {max_value}.")

        return number