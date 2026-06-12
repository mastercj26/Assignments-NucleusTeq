class Student:
    """Class representing a Student."""
    def __init__(self, name: str, roll_number: int):
        self.name = name
        self.roll_number = roll_number

    def display_details(self) -> None:
        print(f"Student Name: {self.name}, Roll Number: {self.roll_number}")


class Car:
    """Class representing a Car."""
    def __init__(self, brand: str, model: str, year: int):
        self.brand = brand
        self.model = model
        self.year = year

    def show_info(self) -> None:
        print(f"Car: {self.year} {self.brand} {self.model}")


class Person:
    """Base class for inheritance."""
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def show_person(self) -> None:
        print(f"Name: {self.name}, Age: {self.age}")


class Employee(Person):
    """Derived class demonstrating inheritance."""
    def __init__(self, name: str, age: int, employee_id: str):
        super().__init__(name, age)
        self.employee_id = employee_id

    def show_employee(self) -> None:
        self.show_person()
        print(f"Employee ID: {self.employee_id}")


class BankAccount:
    """Class demonstrating encapsulation with private variables."""
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.__balance = balance  # Private variable

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.__balance += amount
            print(f"Deposited {amount}. New balance: {self.__balance}")

    def get_balance(self) -> float:
        return self.__balance


# Polymorphism demonstration
class Cat:
    def sound(self) -> str:
        return "Meow"

class Dog:
    def sound(self) -> str:
        return "Bark"

def animal_sound(animal) -> None:
    print(animal.sound())


if __name__ == "__main__":
    # Test OOP
    s = Student("Chetan", 101)
    s.display_details()
    
    c = Car("Toyota", "Camry", 2024)
    c.show_info()
    
    emp = Employee("Alice", 30, "EMP001")
    emp.show_employee()
    
    account = BankAccount("Chetan", 1000)
    account.deposit(500)
    print(f"Balance: {account.get_balance()}")
    
    animal_sound(Cat())
    animal_sound(Dog())
