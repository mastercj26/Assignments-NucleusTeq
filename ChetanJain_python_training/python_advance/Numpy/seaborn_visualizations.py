

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from python_advance.NumPy.constants import (
    EMPLOYEE_NAMES,
    EMPLOYEE_AGES,
    EMPLOYEE_DEPARTMENTS,
    EMPLOYEE_SALARIES,
    FIGURE_WIDTH,
    FIGURE_HEIGHT,
    CHART_DPI,
)


class SeabornBarplotRenderer:


    COLUMN_DEPARTMENT: str = "Department"
    COLUMN_SALARY: str = "Salary"

    def __init__(self, employee_dataframe: pd.DataFrame) -> None:
        self.dataframe = employee_dataframe.copy()

    def render(self) -> None:

        figure, axes = plt.subplots(
            figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), dpi=CHART_DPI
        )
        sns.barplot(
            data=self.dataframe,
            x=self.COLUMN_DEPARTMENT,
            y=self.COLUMN_SALARY,
            ax=axes,
        )
        axes.set_title("Department vs Average Salary")
        axes.set_xlabel("Department")
        axes.set_ylabel("Salary")
        plt.tight_layout()
        plt.show()


class SeabornBoxplotRenderer:


    COLUMN_SALARY: str = "Salary"

    def __init__(self, employee_dataframe: pd.DataFrame) -> None:
        self.dataframe = employee_dataframe.copy()

    def render(self) -> None:

        figure, axes = plt.subplots(
            figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), dpi=CHART_DPI
        )
        sns.boxplot(
            data=self.dataframe,
            y=self.COLUMN_SALARY,
            ax=axes,
        )
        axes.set_title("Salary Distribution (Boxplot)")
        axes.set_ylabel("Salary")
        plt.tight_layout()
        plt.show()


class SeabornHeatmapRenderer:


    COLUMN_AGE: str = "Age"
    COLUMN_SALARY: str = "Salary"

    def __init__(self, employee_dataframe: pd.DataFrame) -> None:
        self.dataframe = employee_dataframe[[self.COLUMN_AGE, self.COLUMN_SALARY]].copy()

    def compute_correlation_matrix(self) -> pd.DataFrame:

        return self.dataframe.corr()

    def render(self) -> None:
        """Display the heatmap."""
        correlation_matrix: pd.DataFrame = self.compute_correlation_matrix()
        figure, axes = plt.subplots(
            figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), dpi=CHART_DPI
        )
        sns.heatmap(
            correlation_matrix,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            ax=axes,
        )
        axes.set_title("Correlation Heatmap: Age vs Salary")
        plt.tight_layout()
        plt.show()


def build_employee_dataframe() -> pd.DataFrame:

    return pd.DataFrame(
        {
            "Name": EMPLOYEE_NAMES,
            "Age": EMPLOYEE_AGES,
            "Department": EMPLOYEE_DEPARTMENTS,
            "Salary": EMPLOYEE_SALARIES,
        }
    )


def run_seaborn_visualizations_demo() -> None:
    """Run all Seaborn visualization demonstrations."""
    employee_dataframe: pd.DataFrame = build_employee_dataframe()

    barplot_renderer = SeabornBarplotRenderer(employee_dataframe)
    barplot_renderer.render()


    boxplot_renderer = SeabornBoxplotRenderer(employee_dataframe)
    boxplot_renderer.render()

    heatmap_renderer = SeabornHeatmapRenderer(employee_dataframe)
    heatmap_renderer.render()