import sys
from python_basic.constants import WELCOME_MESSAGE

def welcome_user() -> None:
    """Prints a welcome message for the training."""
    print(WELCOME_MESSAGE)

def show_python_version() -> None:
    """Shows the current python version installed."""
    print(f"Python version: {sys.version}")

def greet_with_input() -> None:
    """Takes name and age from user and prints a message."""
    name: str = input("Enter your name: ")
    age: str = input("Enter your age: ")
    print(f"Hello {name}, you are {age} years old.")

def demonstrate_types() -> None:
    """Shows different data types in Python."""
    integer_val: int = 10
    float_val: float = 10.5
    string_val: str = "Hello"
    bool_val: bool = True
    
    print(f"Type of {integer_val}: {type(integer_val)}")
    print(f"Type of {float_val}: {type(float_val)}")
    print(f"Type of '{string_val}': {type(string_val)}")
    print(f"Type of {bool_val}: {type(bool_val)}")

def swap_numbers(num1: int, num2: int) -> tuple:
    """Swaps two numbers and returns them."""
    # Using pythonic way for swapping
    num1, num2 = num2, num1
    return num1, num2

def arithmetic_operations(a: float, b: float) -> None:
    """Performs basic math operations on two numbers."""
    print(f"Sum: {a + b}")
    print(f"Difference: {a - b}")
    print(f"Multiplication: {a * b}")
    if b != 0:
        print(f"Division: {a / b}")
    else:
        print("Cannot divide by zero")

# function to check if a number is even or odd
def check_even_odd(num: int) -> str:

    """Checks if a number is even or odd."""
    if num % 2 == 0:
        return "Even"
    return "Odd"

def check_number_status(num: float) -> str:
    """Checks if number is positive, negative or zero."""
    if num > 0:
        return "Positive"
    elif num < 0:
        return "Negative"
    else:
        return "Zero"

def find_largest(a: float, b: float, c: float) -> float:
    """Finds the largest among three numbers."""
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c

def calculate_grade(marks: float) -> str:
    """Returns grade based on marks."""
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 50:
        return "C"
    else:
        return "Fail"

def is_leap_year(year: int) -> bool:
    """Checks if a year is a leap year."""
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False

if __name__ == "__main__":
    # Small test to show it works
    welcome_user()
    show_python_version()
