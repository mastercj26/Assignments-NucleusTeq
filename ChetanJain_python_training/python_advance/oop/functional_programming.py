
from functools import reduce
from typing import Callable


square_lambda: Callable[[int], int] = lambda number: number ** 2


def compute_squares_with_map(number_list: list[int]) -> list[int]:
    """
    Use map() to compute squares of all numbers in number_list.

    Time Complexity: O(n)
    """
    return list(map(lambda number: number ** 2, number_list))


def extract_even_numbers_with_filter(number_list: list[int]) -> list[int]:

    return list(filter(lambda number: number % 2 == 0, number_list))


def compute_product_with_reduce(number_list: list[int]) -> int:

    return reduce(lambda accumulated, current: accumulated * current, number_list)


def compute_factorial_recursive(number: int) -> int:

    if number < 0:
        raise ValueError(f"Factorial is not defined for negative numbers: {number}")
    if number == 0 or number == 1:
        return 1
    return number * compute_factorial_recursive(number - 1)


def compute_fibonacci_recursive(position: int) -> int:

    if position < 0:
        raise ValueError(f"Position must be non-negative: {position}")
    if position == 0:
        return 0
    if position == 1:
        return 1
    return compute_fibonacci_recursive(position - 1) + compute_fibonacci_recursive(position - 2)


def convert_loop_to_functional(number_list: list[int]) -> list[int]:

    even_numbers = filter(lambda number: number % 2 == 0, number_list)
    squared_evens = map(lambda number: number ** 2, even_numbers)
    return list(squared_evens)