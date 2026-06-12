class InsufficientBalanceError(Exception):
    """Custom exception for bank account errors."""
    def __init__(self, message="Balance is not enough for this operation"):
        self.message = message
        super().__init__(self.message)

def test_exception(amount: float) -> None:
    """A small function to test custom exception."""
    if amount < 100:
        raise InsufficientBalanceError(f"Amount {amount} is too low!")
    print("Amount is fine.")

if __name__ == "__main__":
    try:
        test_exception(50)
    except InsufficientBalanceError as e:
        print(f"Caught an error: {e}")
