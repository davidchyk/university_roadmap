from __future__ import annotations

def build_nodes(a: float, b: float, parts: int = 10) -> list[float]:
    h = (b - a) / parts
    return [a + i * h for i in range(parts + 1)]

def calculate_function_values(func, x_nodes: list[float]) -> list[float]:
    return [func(x) for x in x_nodes]

def interpolate_full(x_nodes: list[float], y_nodes: list[float], x: float) -> float:
    table = aitken_table(x_nodes, y_nodes, x)
    return table[0][len(x_nodes) - 1]

def aitken_table(x_nodes: list[float], y_nodes: list[float], x: float) -> list[list[float]]:
    n = len(x_nodes)
    p = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        p[i][0] = y_nodes[i]

    for j in range(1, n):
        for i in range(n - j):
            denominator = x_nodes[i + j] - x_nodes[i]
            if abs(denominator) < 1e-15:
                raise ZeroDivisionError("Zero denominator in Aitken scheme.")
            p[i][j] = (
                (x - x_nodes[i]) * p[i + 1][j - 1]
                - (x - x_nodes[i + j]) * p[i][j - 1]
            ) / denominator

    return p

def aitken_by_degree(x_nodes: list[float], y_nodes: list[float], x: float) -> list[float]:
    approximations: list[float] = []

    for degree in range(len(x_nodes)):
        sub_x = x_nodes[: degree + 1]
        sub_y = y_nodes[: degree + 1]
        table = aitken_table(sub_x, sub_y, x)
        approximations.append(table[0][degree])

    return approximations