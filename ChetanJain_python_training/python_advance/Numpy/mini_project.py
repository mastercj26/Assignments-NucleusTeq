

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from python_advance.NumPy.constants import (
    STUDENT_NAMES,
    STUDENT_MARKS,
    STUDENT_HOURS_STUDIED,
    PASS_MARK_THRESHOLD,
    PASS_LABEL,
    FAIL_LABEL,
    FIGURE_WIDTH,
    FIGURE_HEIGHT,
    CHART_DPI,
    LINE_COLOR,
    SCATTER_COLOR,
)


class StudentDataLoader:


    COLUMN_NAME: str = "Name"
    COLUMN_MARKS: str = "Marks"
    COLUMN_HOURS_STUDIED: str = "Hours Studied"

    def __init__(
        self,
        names: list[str],
        marks: list[int],
        hours_studied: list[int],
    ) -> None:
        self.dataframe: pd.DataFrame = pd.DataFrame(
            {
                self.COLUMN_NAME: names,
                self.COLUMN_MARKS: marks,
                self.COLUMN_HOURS_STUDIED: hours_studied,
            }
        )

    def get_dataframe(self) -> pd.DataFrame:

        return self.dataframe


class StudentPerformanceLabeler:


    COLUMN_MARKS: str = "Marks"
    COLUMN_PERFORMANCE: str = "Performance"

    def __init__(
        self,
        student_dataframe: pd.DataFrame,
        pass_threshold: int,
        pass_label: str,
        fail_label: str,
    ) -> None:
        self.dataframe: pd.DataFrame = student_dataframe.copy()
        self.pass_threshold = pass_threshold
        self.pass_label = pass_label
        self.fail_label = fail_label

    def apply_performance_labels(self) -> None:

        self.dataframe[self.COLUMN_PERFORMANCE] = self.dataframe[
            self.COLUMN_MARKS
        ].apply(
            lambda mark: self.pass_label if mark > self.pass_threshold else self.fail_label
        )

    def get_labeled_dataframe(self) -> pd.DataFrame:

        return self.dataframe


class StudentLineChartRenderer:


    def __init__(
        self,
        hours_studied: pd.Series,
        marks: pd.Series,
    ) -> None:
        self.hours_studied = hours_studied
        self.marks = marks

    def render(self) -> None:

        figure, axes = plt.subplots(
            figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), dpi=CHART_DPI
        )
        axes.plot(
            self.hours_studied,
            self.marks,
            color=LINE_COLOR,
            marker="o",
            linewidth=2,
        )
        axes.set_title("Hours Studied vs Marks (Line Chart)")
        axes.set_xlabel("Hours Studied")
        axes.set_ylabel("Marks")
        plt.tight_layout()
        plt.show()


class StudentScatterPlotRenderer:


    def __init__(
        self,
        hours_studied: pd.Series,
        marks: pd.Series,
    ) -> None:
        self.hours_studied = hours_studied
        self.marks = marks

    def render(self) -> None:

        figure, axes = plt.subplots(
            figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), dpi=CHART_DPI
        )
        axes.scatter(
            self.hours_studied,
            self.marks,
            color=SCATTER_COLOR,
            s=100,
        )
        axes.set_title("Hours Studied vs Marks (Scatter Plot)")
        axes.set_xlabel("Hours Studied")
        axes.set_ylabel("Marks")
        plt.tight_layout()
        plt.show()


class StudentSeabornBarplotRenderer:

    COLUMN_PERFORMANCE: str = "Performance"
    COLUMN_MARKS: str = "Marks"

    def __init__(self, labeled_dataframe: pd.DataFrame) -> None:
        self.dataframe = labeled_dataframe.copy()

    def render(self) -> None:

        figure, axes = plt.subplots(
            figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), dpi=CHART_DPI
        )
        sns.barplot(
            data=self.dataframe,
            x=self.COLUMN_PERFORMANCE,
            y=self.COLUMN_MARKS,
            ax=axes,
        )
        axes.set_title("Performance vs Marks (Seaborn Barplot)")
        axes.set_xlabel("Performance")
        axes.set_ylabel("Marks")
        plt.tight_layout()
        plt.show()


def run_mini_project_demo() -> None:

    data_loader = StudentDataLoader(
        STUDENT_NAMES,
        STUDENT_MARKS,
        STUDENT_HOURS_STUDIED,
    )
    student_dataframe: pd.DataFrame = data_loader.get_dataframe()
    print(student_dataframe)


    performance_labeler = StudentPerformanceLabeler(
        student_dataframe,
        PASS_MARK_THRESHOLD,
        PASS_LABEL,
        FAIL_LABEL,
    )
    performance_labeler.apply_performance_labels()
    labeled_dataframe: pd.DataFrame = performance_labeler.get_labeled_dataframe()
    print(labeled_dataframe)


    line_chart_renderer = StudentLineChartRenderer(
        labeled_dataframe["Hours Studied"],
        labeled_dataframe["Marks"],
    )
    line_chart_renderer.render()


    scatter_renderer = StudentScatterPlotRenderer(
        labeled_dataframe["Hours Studied"],
        labeled_dataframe["Marks"],
    )
    scatter_renderer.render()

    seaborn_barplot_renderer = StudentSeabornBarplotRenderer(labeled_dataframe)
    seaborn_barplot_renderer.render()