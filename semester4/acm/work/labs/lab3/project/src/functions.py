from __future__ import annotations

import math
from typing import Callable

def target_function(x: float) -> float:
    return math.sin(x ** 2) * math.exp(-((x / 2) ** 2))

def test_function(x: float) -> float:
    return math.sin(x)

def get_function_by_name(name: str) -> tuple[Callable[[float], float], str]:
    if name == "test":
        return test_function, "sin(x)"
    return target_function, "sin(x^2) * exp(-(x/2)^2)"