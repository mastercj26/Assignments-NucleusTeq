
import numpy as np
import pandas as pd
from python_advance.NumPy.constants import MISSING_SALARY_REPLACEMENT


class DataCleaner:


    COLUMN_NAME: str = "Name"
    COLUMN_AGE: str = "Age"
    COLUMN_SALARY: str = "Salary"

    def __init__(self, raw_dataframe: pd.DataFrame) -> None:
        self.dataframe: pd.DataFrame = raw_dataframe.copy()

    def detect_missing_values(self) -> pd.DataFrame:

        return self.dataframe.isnull()

    def fill_age_with_mean(self) -> None:

        age_mean: float = self.dataframe[self.COLUMN_AGE].mean()
        self.dataframe[self.COLUMN_AGE] = self.dataframe[self.COLUMN_AGE].fillna(
            age_mean
        )

    def fill_salary_with_zero(self) -> None:

        self.dataframe[self.COLUMN_SALARY] = self.dataframe[
            self.COLUMN_SALARY
        ].fillna(MISSING_SALARY_REPLACEMENT)

    def get_cleaned_dataframe(self) -> pd.DataFrame:

        return self.dataframe


def build_dirty_dataframe() -> pd.DataFrame:

    raw_data: dict = {
        "Name": ["Rahul", "Priya", "Anuj"],
        "Age": [25.0, np.nan, 29.0],
        "Salary": [30000.0, 40000.0, np.nan],
    }
    return pd.DataFrame(raw_data)


def run_data_cleaning_demo() -> None:

    dirty_dataframe: pd.DataFrame = build_dirty_dataframe()

    data_cleaner = DataCleaner(dirty_dataframe)


    print(data_cleaner.detect_missing_values())

    data_cleaner.fill_age_with_mean()
    data_cleaner.fill_salary_with_zero()


    print(data_cleaner.get_cleaned_dataframe())