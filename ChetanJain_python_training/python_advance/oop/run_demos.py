

from python_advance.oop.models import (
    validate_age,
    validate_positive_number,
    open_file_safely,
    divide_two_numbers,
)
from python_advance.oop.iterators_generators import (
    NumberRangeIterator,
    generate_fibonacci_sequence,
    get_even_number_generator,
    process_large_dataset_with_generator,
)
from python_advance.oop.functional_programming import (
    square_lambda,
    compute_squares_with_map,
    extract_even_numbers_with_filter,
    compute_product_with_reduce,
    compute_factorial_recursive,
)
from python_advance.oop.regex_operations import (
    validate_email_address,
    validate_password_strength,
    extract_numbers_from_string,
)
from python_advance.oop.packaging_demo import add_numbers, divide_numbers


if __name__ == "__main__":
    print("=== Exception Handling ===")
    try:
        validate_age(15)
    except Exception as error:
        print(error)

    print("\n=== Iterators ===")
    for number in NumberRangeIterator(5):
        print(number)

    print("\n=== Fibonacci Generator ===")
    fibonacci_generator = generate_fibonacci_sequence()
    for _ in range(8):
        print(next(fibonacci_generator))

    print("\n=== Functional Programming ===")
    print(square_lambda(9))
    print(compute_squares_with_map([1, 2, 3, 4, 5]))
    print(extract_even_numbers_with_filter([1, 2, 3, 4, 5, 6]))
    print(compute_product_with_reduce([1, 2, 3, 4, 5]))
    print(compute_factorial_recursive(6))

    print("\n=== Regex ===")
    print(validate_email_address("user@example.com"))
    print(validate_password_strength("Secure@123"))
    print(extract_numbers_from_string("I have 3 cats and 12 dogs"))

    print("\n=== Packaging ===")
    print(add_numbers(10, 20))
    print(divide_numbers(100, 4))

    print("\n=== Large Dataset Generator ===")
    total = process_large_dataset_with_generator(1000000)
    print(f"Sum of 1M numbers: {total}")