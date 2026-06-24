

import pandas as pd
from python_advance.NumPy.constants import (
    EMPLOYEE_NAMES,
    EMPLOYEE_AGES,
    EMPLOYEE_DEPARTMENTS,
    EMPLOYEE_SALARIES,
)


class EmployeeGroupAnalyzer:


    COLUMN_NAME: str = "Name"
    COLUMN_AGE: str = "Age"
    COLUMN_DEPARTMENT: str = "Department"
    COLUMN_SALARY: str = "Salary"

    def __init__(self, employee_dataframe: pd.DataFrame) -> None:
        self.dataframe: pd.DataFrame = employee_dataframe.copy()

    def compute_average_salary_by_department(self) -> pd.Series:

        return self.dataframe.groupby(self.COLUMN_DEPARTMENT)[
            self.COLUMN_SALARY
        ].mean()

    def compute_max_salary_by_department(self) -> pd.Series:

        return self.dataframe.groupby(self.COLUMN_DEPARTMENT)[
            self.COLUMN_SALARY
        ].max()

    def count_employees_per_department(self) -> pd.Series:

        return self.dataframe.groupby(self.COLUMN_DEPARTMENT)[
            self.COLUMN_NAME
        ].count()


def build_employee_dataframe() -> pd.DataFrame:

    return pd.DataFrame(
        {
            "Name": EMPLOYEE_NAMES,
            "Age": EMPLOYEE_AGES,
            "Department": EMPLOYEE_DEPARTMENTS,
            "Salary": EMPLOYEE_SALARIES,
        }
    )


def run_data_analysis_demo() -> None:

    employee_dataframe: pd.DataFrame = build_employee_dataframe()
    group_analyzer = EmployeeGroupAnalyzer(employee_dataframe)


    print(group_analyzer.compute_average_salary_by_department())


    print(group_analyzer.compute_max_salary_by_department())


    print(group_analyzer.count_employees_per_department())