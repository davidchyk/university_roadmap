from __future__ import annotations

from src.aitken import aitken_by_degree
from src.models import ErrorRow

def compute_error_rows(func, x_nodes: list[float], y_nodes: list[float], x_value: float) -> tuple[float, list[ErrorRow]]:
    true_value = func(x_value)
    approximations = aitken_by_degree(x_nodes, y_nodes, x_value)

    rows: list[ErrorRow] = []
    for degree, approx in enumerate(approximations):
        estimate = None if degree == 0 else abs(approximations[degree] - approximations[degree - 1])
        actual_error = abs(true_value - approx)
        rows.append(
            ErrorRow(
                degree=degree,
                approximation=approx,
                estimate=estimate,
                actual_error=actual_error,
            )
        )
    return true_value, rows