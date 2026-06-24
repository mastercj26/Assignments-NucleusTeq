

import matplotlib.pyplot as plt
from python_advance.NumPy.constants import (
    DEPARTMENT_NAMES,
    DEPARTMENT_EMPLOYEE_COUNTS,
    SALARY_DATA,
    EMPLOYEE_AGES,
    EMPLOYEE_SALARIES,
    FIGURE_WIDTH,
    FIGURE_HEIGHT,
    BAR_COLOR,
    LINE_COLOR,
    SCATTER_COLOR,
    CHART_DPI,
)


class BarChartPlotter:


    def __init__(
        self,
        category_labels: list[str],
        numeric_values: list[int],
        chart_title: str,
        x_axis_label: str,
        y_axis_label: str,
    ) -> None:
        self.category_labels = category_labels
        self.numeric_values = numeric_values
        self.chart_title = chart_title
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label

    def render(self) -> None:
        """Render and display the bar chart."""
        figure, axes = plt.subplots(
            figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), dpi=CHART_DPI
        )
        axes.bar(self.category_labels, self.numeric_values, color=BAR_COLOR)
        axes.set_title(self.chart_title)
        axes.set_xlabel(self.x_axis_label)
        axes.set_ylabel(self.y_axis_label)
        plt.tight_layout()
        plt.show()


class LineChartPlotter:


    def __init__(
        self,
        x_values: list,
        y_values: list,
        chart_title: str,
        x_axis_label: str,
        y_axis_label: str,
    ) -> None:
        self.x_values = x_values
        self.y_values = y_values
        self.chart_title = chart_title
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label

    def render(self) -> None:

        figure, axes = plt.subplots(
            figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), dpi=CHART_DPI
        )
        axes.plot(
            self.x_values,
            self.y_values,
            color=LINE_COLOR,
            marker="o",
            linewidth=2,
        )
        axes.set_title(self.chart_title)
        axes.set_xlabel(self.x_axis_label)
        axes.set_ylabel(self.y_axis_label)
        plt.tight_layout()
        plt.show()


class HistogramPlotter:

    def __init__(
        self,
        salary_values: list[int],
        bin_count: int,
        chart_title: str,
        x_axis_label: str,
        y_axis_label: str,
    ) -> None:
        self.salary_values = salary_values
        self.bin_count = bin_count
        self.chart_title = chart_title
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label

    def render(self) -> None:

        figure, axes = plt.subplots(
            figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), dpi=CHART_DPI
        )
        axes.hist(self.salary_values, bins=self.bin_count, color=BAR_COLOR, edgecolor="black")
        axes.set_title(self.chart_title)
        axes.set_xlabel(self.x_axis_label)
        axes.set_ylabel(self.y_axis_label)
        plt.tight_layout()
        plt.show()


class ScatterPlotPlotter:


    def __init__(
        self,
        x_values: list,
        y_values: list,
        chart_title: str,
        x_axis_label: str,
        y_axis_label: str,
    ) -> None:
        self.x_values = x_values
        self.y_values = y_values
        self.chart_title = chart_title
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label

    def render(self) -> None:
        figure, axes = plt.subplots(
            figsize=(FIGURE_WIDTH, FIGURE_HEIGHT), dpi=CHART_DPI
        )
        axes.scatter(self.x_values, self.y_values, color=SCATTER_COLOR, s=100)
        axes.set_title(self.chart_title)
        axes.set_xlabel(self.x_axis_label)
        axes.set_ylabel(self.y_axis_label)
        plt.tight_layout()
        plt.show()


def run_matplotlib_charts_demo() -> None:

    print("===== Bar Chart =====")
    bar_plotter = BarChartPlotter(
        DEPARTMENT_NAMES,
        DEPARTMENT_EMPLOYEE_COUNTS,
        "Employees per Department",
        "Department",
        "Number of Employees",
    )
    bar_plotter.render()


    line_plotter = LineChartPlotter(
        DEPARTMENT_NAMES,
        DEPARTMENT_EMPLOYEE_COUNTS,
        "Employee Count Trend by Department",
        "Department",
        "Number of Employees",
    )
    line_plotter.render()

    histogram_plotter = HistogramPlotter(
        SALARY_DATA,
        bin_count=5,
        chart_title="Salary Distribution",
        x_axis_label="Salary",
        y_axis_label="Frequency",
    )
    histogram_plotter.render()


    scatter_plotter = ScatterPlotPlotter(
        EMPLOYEE_AGES,
        EMPLOYEE_SALARIES,
        "Age vs Salary",
        "Age",
        "Salary",
    )
    scatter_plotter.render()