def print_1_to_100() -> None:
    """Prints numbers from 1 to 100."""
    for i in range(1, 101):
        print(i, end=" ")
    print()

def print_table(n: int) -> None:
    """Prints multiplication table of a number."""
    for i in range(1, 11):
        print(f"{n} x {i} = {n * i}")

def find_factorial(n: int) -> int:
    """Finds factorial using a loop."""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def reverse_number(n: int) -> int:
    """Reverses a number using a loop."""
    reversed_num = 0
    temp = n
    print(f"Reversing number: {n}")
    while temp > 0:

        digit = temp % 10
        reversed_num = reversed_num * 10 + digit
        temp //= 10
    return reversed_num

def check_prime(n: int) -> bool:
    """Checks if a number is prime."""
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    print("Factorial of 5:", find_factorial(5))
    print("Reverse of 123:", reverse_number(123))
    print("Is 7 prime?", check_prime(7))
