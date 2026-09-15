from __future__ import annotations

from src.models import ErrorRow, RootResult


def build_error_rows(results: list[RootResult]) -> list[ErrorRow]:
    return [
        ErrorRow(
            index=index,
            interval=result.interval,
            root=result.root,
            function_value=result.function_value,
            estimated_error=result.estimated_error,
            iterations=result.iterations,
        )
        for index, result in enumerate(results, start=1)
    ]


def max_residual(results: list[RootResult]) -> float:
    if not results:
        return 0.0
    return max(abs(result.function_value) for result in results)


def max_estimated_error(results: list[RootResult]) -> float:
    if not results:
        return 0.0
    return max(result.estimated_error for result in results)
