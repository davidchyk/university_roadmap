from __future__ import annotations

from src.models import ErrorRow


def format_float(value: float | None, digits: int = 10) -> str:
    if value is None:
        return "-"
    return f"{value:.{digits}f}"


def build_short_result(rows: list[ErrorRow], true_value: float) -> str:
    best = rows[-1]
    return (
        f"f(x) = {true_value:.10f}\n"
        f"P_{best.degree}(x) = {best.approximation:.10f}\n"
        f"Estimate = {format_float(best.estimate, 10)}\n"
        f"Actual error = {best.actual_error:.10f}"
    )


def build_full_report(
    func_name: str,
    a: float,
    b: float,
    x_value: float,
    x_nodes: list[float],
    y_nodes: list[float],
    rows: list[ErrorRow],
    true_value: float,
) -> str:
    lines: list[str] = []

    lines.append("Aitken interpolation report")
    lines.append("=" * 78)
    lines.append(f"Function: {func_name}")
    lines.append(f"Interval: [{a}, {b}]")
    lines.append(f"x = {x_value}")
    lines.append(f"f(x) = {true_value:.12f}")
    lines.append("")

    lines.append("Nodes:")
    lines.append("i        x_i                y_i")
    lines.append("-" * 48)
    for i, (x_i, y_i) in enumerate(zip(x_nodes, y_nodes)):
        lines.append(f"{i:<8}{x_i:<18.10f}{y_i:<18.10f}")

    lines.append("")
    lines.append("Errors by polynomial degree:")
    lines.append("n        P_n(x)             |P_n - P_(n-1)|      |f(x)-P_n(x)|")
    lines.append("-" * 78)
    for row in rows:
        lines.append(
            f"{row.degree:<8}"
            f"{row.approximation:<20.10f}"
            f"{format_float(row.estimate, 10):<20}"
            f"{row.actual_error:<20.10f}"
        )

    return "\n".join(lines)