from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from src.models import RootInterval, RootResult


Function = Callable[[float], float]


@dataclass(frozen=True)
class PlotData:
    x_values: list[float]
    y_values: list[float]
    intervals: list[RootInterval]
    results: list[RootResult]
    left: float
    right: float
    y_min: float
    y_max: float


def build_function_plot_data(
    func: Function,
    intervals: list[RootInterval],
    results: list[RootResult],
    left: float,
    right: float,
    plot_points: int,
) -> PlotData:
    if plot_points < 50:
        raise ValueError("Кількість точок графіка має бути не меншою за 50.")

    x_values = _build_x_values(left, right, plot_points)
    y_values = [func(x_value) for x_value in x_values]
    y_min = min(min(y_values), 0.0)
    y_max = max(max(y_values), 0.0)

    if y_min == y_max:
        y_min -= 1.0
        y_max += 1.0

    padding = (y_max - y_min) * 0.08
    return PlotData(
        x_values=x_values,
        y_values=y_values,
        intervals=intervals,
        results=results,
        left=left,
        right=right,
        y_min=y_min - padding,
        y_max=y_max + padding,
    )


def _build_x_values(left: float, right: float, points: int) -> list[float]:
    step = (right - left) / (points - 1)
    return [left + index * step for index in range(points)]
