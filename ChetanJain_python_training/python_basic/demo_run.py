from python_basic.basics import welcome_user, is_leap_year
from python_basic.loops import find_factorial
from python_basic.functions_demo import is_palindrome
from python_basic.my_module import my_custom_function

def run_demos():
    print("--- Welcome Demo ---")
    welcome_user()
    
    print("\n--- Leap Year Demo ---")
    print(f"Is 2024 a leap year? {is_leap_year(2024)}")
    
    print("\n--- Factorial Demo ---")
    print(f"Factorial of 6 is {find_factorial(6)}")
    
    print("\n--- Palindrome Demo ---")
    print(f"Is 'racecar' a palindrome? {is_palindrome('racecar')}")
    
    print("\n--- Custom Module Demo ---")
    print(my_custom_function())

if __name__ == "__main__":
    run_demos()
