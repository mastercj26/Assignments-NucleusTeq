

import pytest
from python_advance.oop.packaging_demo.math_operations import add_numbers


def is_prime_number(number: int) -> bool:
    """
    Check whether number is a prime number.

    Time Complexity: O(sqrt(n))
    """
    if number < 2:
        return False
    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False
    return True


class TestAddNumbers:
    """Test cases for add_numbers() function."""

    def test_add_two_positive_integers(self) -> None:

        assert add_numbers(3, 5) == 8

    def test_add_positive_and_negative_integer(self) -> None:

        assert add_numbers(10, -3) == 7

    def test_add_two_float_numbers(self) -> None:

        assert add_numbers(1.5, 2.5) == 4.0

    def test_add_zero_to_number(self) -> None:

        assert add_numbers(7, 0) == 7

    def test_add_two_negative_integers(self) -> None:

        assert add_numbers(-4, -6) == -10


class TestIsPrimeNumber:


    def test_number_two_is_prime(self) -> None:

        assert is_prime_number(2) is True

    def test_number_three_is_prime(self) -> None:
        """Test that 3 is recognized as prime."""
        assert is_prime_number(3) is True

    def test_number_one_is_not_prime(self) -> None:

        assert is_prime_number(1) is False

    def test_negative_number_is_not_prime(self) -> None:

        assert is_prime_number(-5) is False

    def test_composite_number_is_not_prime(self) -> None:

        assert is_prime_number(9) is False

    def test_large_prime_number(self) -> None:

        assert is_prime_number(97) is True

    def test_even_number_greater_than_two_is_not_prime(self) -> None:

        assert is_prime_number(4) is False


def function_with_logical_bug(number_list: list[int]) -> int:

    import pdb
    product_accumulator: int = 0
    pdb.set_trace()
    for number in number_list:
        product_accumulator *= number
    return product_accumulator


def demonstrate_pdb_in_loop(number_list: list[int]) -> None:

    import pdb
    running_total: int = 0
    for current_number in number_list:
        pdb.set_trace()
        running_total += current_number
    print(f"Final total: {running_total}")


