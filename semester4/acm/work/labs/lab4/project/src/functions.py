from __future__ import annotations

import math
from collections.abc import Callable


Function = Callable[[float], float]


def target_function(x_value: float) -> float:
    return math.pow(2.0, x_value) - 4.0 * x_value


def get_function_by_name(function_name: str) -> tuple[Function, str]:
    functions: dict[str, tuple[Function, str]] = {
        "target": (target_function, "2^x - 4x = 0"),
    }

    try:
        return functions[function_name]
    except KeyError as exc:
        raise ValueError(f"Невідома функція: {function_name}") from exc
