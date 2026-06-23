"""
Mathematical utility functions module.

Provides: add, subtract, multiply, divide operations.
"""

from typing import Union

Number = Union[int, float]


def add_numbers(first_number: Number, second_number: Number) -> Number:

    return first_number + second_number


def subtract_numbers(first_number: Number, second_number: Number) -> Number:

    return first_number - second_number


def multiply_numbers(first_number: Number, second_number: Number) -> Number:

    return first_number * second_number


def divide_numbers(dividend: Number, divisor: Number) -> float:

    if divisor == 0:
        raise ZeroDivisionError("Divisor cannot be zero.")
    return dividend / divisor