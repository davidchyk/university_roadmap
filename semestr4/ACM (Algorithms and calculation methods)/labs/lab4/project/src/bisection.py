from __future__ import annotations

from collections.abc import Callable

from src.models import IterationRow, RootInterval, RootResult


Function = Callable[[float], float]


def isolate_root_intervals(
    func: Function,
    left: float,
    right: float,
    scan_step: float,
    zero_tolerance: float = 1e-12,
) -> list[RootInterval]:
    if right <= left:
        raise ValueError("Права межа має бути більшою за ліву.")
    if scan_step <= 0:
        raise ValueError("Крок відокремлення коренів має бути додатним.")

    intervals: list[RootInterval] = []
    x_left = left
    f_left = func(x_left)

    if abs(f_left) <= zero_tolerance:
        intervals.append(RootInterval(x_left, x_left))

    while x_left < right:
        x_right = min(x_left + scan_step, right)
        f_right = func(x_right)

        if abs(f_right) <= zero_tolerance:
            intervals.append(RootInterval(x_right, x_right))
        elif f_left * f_right < 0:
            intervals.append(RootInterval(x_left, x_right))

        x_left = x_right
        f_left = f_right

    return _deduplicate_intervals(intervals, zero_tolerance)


def solve_bisection(
    func: Function,
    interval: RootInterval,
    epsilon: float,
    max_iterations: int,
) -> RootResult:
    if epsilon <= 0:
        raise ValueError("Точність epsilon має бути додатною.")
    if max_iterations < 1:
        raise ValueError("Максимальна кількість ітерацій має бути не меншою за 1.")

    left = interval.left
    right = interval.right
    f_left = func(left)
    f_right = func(right)

    if abs(f_left) <= epsilon:
        return RootResult(interval, left, f_left, 0, 0.0, [])
    if abs(f_right) <= epsilon:
        return RootResult(interval, right, f_right, 0, 0.0, [])
    if f_left * f_right > 0:
        raise ValueError(
            "На проміжку немає зміни знака функції, тому метод половинного "
            "ділення не може бути застосований."
        )

    history: list[IterationRow] = []

    for iteration in range(1, max_iterations + 1):
        midpoint = (left + right) / 2.0
        f_midpoint = func(midpoint)
        interval_length = abs(right - left)
        estimated_error = interval_length / 2.0

        history.append(
            IterationRow(
                iteration=iteration,
                left=left,
                right=right,
                midpoint=midpoint,
                f_left=f_left,
                f_midpoint=f_midpoint,
                interval_length=interval_length,
                estimated_error=estimated_error,
            )
        )

        if abs(f_midpoint) <= epsilon or estimated_error <= epsilon:
            return RootResult(
                interval=interval,
                root=midpoint,
                function_value=f_midpoint,
                iterations=iteration,
                estimated_error=estimated_error,
                history=history,
            )

        if f_left * f_midpoint < 0:
            right = midpoint
        else:
            left = midpoint
            f_left = f_midpoint

    root = (left + right) / 2.0
    return RootResult(
        interval=interval,
        root=root,
        function_value=func(root),
        iterations=max_iterations,
        estimated_error=abs(right - left) / 2.0,
        history=history,
    )


def solve_all_intervals(
    func: Function,
    intervals: list[RootInterval],
    epsilon: float,
    max_iterations: int,
) -> list[RootResult]:
    return [
        solve_bisection(func, interval, epsilon, max_iterations)
        for interval in intervals
    ]


def _deduplicate_intervals(
    intervals: list[RootInterval],
    zero_tolerance: float,
) -> list[RootInterval]:
    unique: list[RootInterval] = []

    for interval in intervals:
        is_duplicate = any(
            abs(interval.left - item.left) <= zero_tolerance
            and abs(interval.right - item.right) <= zero_tolerance
            for item in unique
        )
        if not is_duplicate:
            unique.append(interval)

    return unique
