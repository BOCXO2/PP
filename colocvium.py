from typing import List
import unittest


def fibonacci_sequence(n: int) -> List[int]:
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n <= 0:
        raise ValueError("Input must be a positive integer.")
    
    if n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for _ in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence


class TestFibonacciSequence(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(fibonacci_sequence(1), [0])
        self.assertEqual(fibonacci_sequence(2), [0, 1])
        self.assertEqual(fibonacci_sequence(5), [0, 1, 1, 2, 3])
        self.assertEqual(fibonacci_sequence(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])
    
    def test_invalid_input_type(self):
        with self.assertRaises(TypeError):
            fibonacci_sequence("10")
        with self.assertRaises(TypeError):
            fibonacci_sequence(10.5)
    
    def test_invalid_input_value(self):
        with self.assertRaises(ValueError):
            fibonacci_sequence(0)
        with self.assertRaises(ValueError):
            fibonacci_sequence(-5)


if __name__ == "__main__":
    choice = input("Enter 'test' to run unit tests or 'run' to provide input: ").strip().lower()
    if choice == "test":
        unittest.main()
    elif choice == "run":
        try:
            n = int(input("Enter a positive integer: "))
            print(f"The first {n} Fibonacci numbers are: {fibonacci_sequence(n)}")
        except (TypeError, ValueError) as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice. Please enter 'test' or 'run'.")
