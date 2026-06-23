

from typing import Generator, Iterator
from python_advance.constants import (
    FIBONACCI_START_A,
    FIBONACCI_START_B,
    LARGE_DATASET_SIZE,
    SQUARE_LIMIT,
    EVEN_NUMBER_LIMIT,
)


class NumberRangeIterator:


    def __init__(self, upper_limit: int) -> None:
        self.upper_limit = upper_limit
        self.current_number = 1

    def __iter__(self) -> "NumberRangeIterator":
        return self

    def __next__(self) -> int:
        if self.current_number > self.upper_limit:
            raise StopIteration
        yielded_number: int = self.current_number
        self.current_number += 1
        return yielded_number


def iterate_list_with_next(input_list: list) -> None:

    list_iterator: Iterator = iter(input_list)
    try:
        while True:
            element = next(list_iterator)
            print(element)
    except StopIteration:
        print("All elements exhausted.")


def generate_square_numbers(upper_limit: int) -> Generator[int, None, None]:

    for number in range(1, upper_limit + 1):
        yield number ** 2


def generate_fibonacci_sequence() -> Generator[int, None, None]:

    previous_number: int = FIBONACCI_START_A
    current_number: int = FIBONACCI_START_B
    while True:
        yield previous_number
        previous_number, current_number = current_number, previous_number + current_number


def get_even_number_generator(upper_limit: int) -> Generator[int, None, None]:

    return (number for number in range(1, upper_limit + 1) if number % 2 == 0)


def process_large_dataset_with_generator(dataset_size: int) -> int:

    def large_number_generator(size: int) -> Generator[int, None, None]:
        for index in range(size):
            yield index

    total_sum: int = sum(large_number_generator(dataset_size))
    return total_sum


def demonstrate_builtin_generator_range(start: int, stop: int) -> None:

    number_range = range(start, stop)
    for number in number_range:
        print(number)


def explain_iterator_vs_generator() -> None:

    explanation: str =