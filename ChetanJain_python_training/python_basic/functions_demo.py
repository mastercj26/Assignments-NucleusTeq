import math
import random

def calculate_square(n: float) -> float:
    """Calculates square of a number."""
    return n * n

def is_palindrome(data) -> bool:
    """Checks if string or number is palindrome."""
    # Convert to string to handle both cases
    s = str(data)
    return s == s[::-1]

def find_max_in_list(numbers: list) -> float:
    """Returns maximum number from a list."""
    if not numbers:
        return 0.0
    return max(numbers)

def greet_person(name: str, message: str = "Welcome to Python Training") -> str:
    """Function with default parameters."""
    return f"Hello {name}, {message}"

def math_module_usage() -> None:
    """Demonstrates math module functions."""
    num = 16
    print(f"Square root of {num}: {math.sqrt(num)}")
    print(f"Power 2^3: {math.pow(2, 3)}")
    print(f"Factorial of 5: {math.factorial(5)}")

def random_module_usage() -> None:
    """Demonstrates random module functions."""
    print(f"Random int between 1 and 100: {random.randint(1, 100)}")

if __name__ == "__main__":
    print(is_palindrome("madam"))
    print(is_palindrome(121))
    math_module_usage()
    random_module_usage()
