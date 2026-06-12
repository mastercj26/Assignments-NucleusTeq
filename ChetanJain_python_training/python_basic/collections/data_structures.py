def list_operations() -> None:
    """Performs various operations on a list of 10 numbers."""
    numbers = [10, 20, 5, 45, 99, 10, 20, 7, 8, 15]
    
    print(f"Original list: {numbers}")
    print(f"Sum: {sum(numbers)}")
    print(f"Max: {max(numbers)}")
    
    # Remove duplicates
    unique_numbers = []
    for num in numbers:
        if num not in unique_numbers:
            unique_numbers.append(num)
    print(f"List after removing duplicates: {unique_numbers}")
    
    # Sort
    unique_numbers.sort()
    print(f"Sorted list: {unique_numbers}")

def count_even_odd_in_list(numbers: list) -> None:
    """Counts even and odd numbers in a list."""
    even_count = 0
    odd_count = 0
    for num in numbers:
        if num % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
    print(f"Even numbers: {even_count}, Odd numbers: {odd_count}")

def reverse_list_manually(numbers: list) -> list:
    """Reverses a list without using reverse() method."""
    reversed_list = []
    for i in range(len(numbers) - 1, -1, -1):
        reversed_list.append(numbers[i])
    return reversed_list

def tuple_and_list_demo() -> None:
    """Demonstrates tuple operations and conversion."""
    # Create tuple and access
    my_tuple = (1, 2, 3, "Python", True)
    print(f"Tuple: {my_tuple}, First element: {my_tuple[0]}")
    
    # Convert to list and modify
    my_list = list(my_tuple)
    my_list[0] = 100
    print(f"Modified list from tuple: {my_list}")

def set_operations() -> None:
    """Demonstrates union, intersection, and difference on sets."""
    set1 = {1, 2, 3, 4, 5}
    set2 = {4, 5, 6, 7, 8}
    
    print(f"Union: {set1 | set2}")
    print(f"Intersection: {set1 & set2}")
    print(f"Difference (set1 - set2): {set1 - set2}")

def remove_duplicates_with_set(numbers: list) -> list:
    """Removes duplicates from a list using a set."""
    return list(set(numbers))

def dictionary_demo() -> None:
    """Demonstrates dictionary operations."""
    # Student dictionary
    student = {
        "name": "Chetan",
        "age": 21,
        "course": "Python Training"
    }
    print(f"Student name: {student['name']}")
    
    # Character frequency
    text = "hello world"
    freq = {}
    for char in text:
        if char != " ":
            freq[char] = freq.get(char, 0) + 1
    print(f"Character frequency: {freq}")
    
    # Merge dictionaries
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    # Using update or union operator
    dict1.update(dict2)
    print(f"Merged dictionary: {dict1}")

if __name__ == "__main__":
    list_operations()
    tuple_and_list_demo()
    set_operations()
    dictionary_demo()
