
import pandas as pd
from python_advance.NumPy.constants import (
    EMPLOYEE_NAMES,
    EMPLOYEE_AGES,
    EMPLOYEE_DEPARTMENTS,
    EMPLOYEE_SALARIES,
    BONUS_RATE,
    IT_DEPARTMENT_LABEL,
)


class EmployeeDataFrame:


    COLUMN_NAME: str = "Name"
    COLUMN_AGE: str = "Age"
    COLUMN_DEPARTMENT: str = "Department"
    COLUMN_SALARY: str = "Salary"
    COLUMN_BONUS: str = "Bonus"

    def __init__(
        self,
        names: list[str],
        ages: list[int],
        departments: list[str],
        salaries: list[int],
    ) -> None:
        self.dataframe: pd.DataFrame = pd.DataFrame(
            {
                self.COLUMN_NAME: names,
                self.COLUMN_AGE: ages,
                self.COLUMN_DEPARTMENT: departments,
                self.COLUMN_SALARY: salaries,
            }
        )

    def get_first_n_rows(self, row_count: int = 2) -> pd.DataFrame:

        return self.dataframe.head(row_count)

    def get_summary_statistics(self) -> pd.DataFrame:

        return self.dataframe.describe()

    def filter_by_department(self, department_name: str) -> pd.DataFrame:

        return self.dataframe[
            self.dataframe[self.COLUMN_DEPARTMENT] == department_name
        ]

    def add_bonus_column(self, bonus_rate: float) -> None:

        self.dataframe[self.COLUMN_BONUS] = (
            self.dataframe[self.COLUMN_SALARY] * bonus_rate
        )

    def display_all(self) -> None:
        """Print the complete DataFrame."""
        print(self.dataframe.to_string(index=False))


def run_pandas_dataframe_demo() -> None:
    """Run all Pandas DataFrame demonstrations."""
    employee_df = EmployeeDataFrame(
        EMPLOYEE_NAMES,
        EMPLOYEE_AGES,
        EMPLOYEE_DEPARTMENTS,
        EMPLOYEE_SALARIES,
    )

    print("===== First 2 Rows =====")
    print(employee_df.get_first_n_rows(2))

    print("\n===== Summary Statistics =====")
    print(employee_df.get_summary_statistics())

    print(f"\n===== {IT_DEPARTMENT_LABEL} Employees =====")
    print(employee_df.filter_by_department(IT_DEPARTMENT_LABEL))

    employee_df.add_bonus_column(BONUS_RATE)
    print("\n===== DataFrame with Bonus Column =====")
    employee_df.display_all()