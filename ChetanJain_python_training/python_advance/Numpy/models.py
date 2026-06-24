

import numpy as np
from numpy.typing import NDArray
from python_advance.NumPy.constants import (
    SAMPLE_ARRAY,
    ARRAY_ONE,
    ARRAY_TWO,
    MATRIX_ROWS,
    MATRIX_COLS,
    MATRIX_START_VALUE,
    MATRIX_END_VALUE,
)


class NumpyArrayAnalyzer:


    def __init__(self, raw_data: list[int]) -> None:
        self.numpy_array: NDArray[np.int_] = np.array(raw_data)

    def compute_mean(self) -> float:

        return float(np.mean(self.numpy_array))

    def compute_max(self) -> int:

        return int(np.max(self.numpy_array))

    def compute_min(self) -> int:

        return int(np.min(self.numpy_array))

    def compute_sum(self) -> int:

        return int(np.sum(self.numpy_array))

    def display_statistics(self) -> None:

        print(f"Array      : {self.numpy_array}")
        print(f"Mean       : {self.compute_mean()}")
        print(f"Max        : {self.compute_max()}")
        print(f"Min        : {self.compute_min()}")
        print(f"Sum        : {self.compute_sum()}")


class NumpyArrayArithmetic:


    def __init__(
        self,
        first_array_data: list[int],
        second_array_data: list[int],
    ) -> None:
        self.first_array: NDArray[np.int_] = np.array(first_array_data)
        self.second_array: NDArray[np.int_] = np.array(second_array_data)

    def compute_addition(self) -> NDArray[np.int_]:
        """Return element-wise addition of both arrays."""
        return self.first_array + self.second_array

    def compute_multiplication(self) -> NDArray[np.int_]:
        """Return element-wise multiplication of both arrays."""
        return self.first_array * self.second_array

    def display_arithmetic_results(self) -> None:
        """Print addition and multiplication results."""
        print(f"Array 1         : {self.first_array}")
        print(f"Array 2         : {self.second_array}")
        print(f"Addition        : {self.compute_addition()}")
        print(f"Multiplication  : {self.compute_multiplication()}")


class NumpyMatrixCreator:


    def __init__(self, rows: int, cols: int, start: int, end: int) -> None:
        self.rows = rows
        self.cols = cols
        self.start = start
        self.end = end

    def create_matrix(self) -> NDArray[np.int_]:

        total_elements: int = self.rows * self.cols
        flat_array: NDArray[np.int_] = np.arange(
            self.start, self.start + total_elements
        )
        return flat_array.reshape(self.rows, self.cols)

    def display_matrix(self) -> None:
        """Print the created matrix."""
        matrix: NDArray[np.int_] = self.create_matrix()
        print(f"{self.rows}x{self.cols} Matrix:\n{matrix}")


def run_numpy_basics_demo() -> None:
    """Run all NumPy basic demonstrations."""

    array_analyzer = NumpyArrayAnalyzer(SAMPLE_ARRAY)
    array_analyzer.display_statistics()


    array_arithmetic = NumpyArrayArithmetic(ARRAY_ONE, ARRAY_TWO)
    array_arithmetic.display_arithmetic_results()


    matrix_creator = NumpyMatrixCreator(
        MATRIX_ROWS, MATRIX_COLS, MATRIX_START_VALUE, MATRIX_END_VALUE
    )
    matrix_creator.display_matrix()