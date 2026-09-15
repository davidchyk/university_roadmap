from __future__ import annotations

import random
from collections.abc import Callable

from matplotlib.figure import Figure


def build_actual_vs_theoretical_figure(
    sort_func: Callable[[list[int]], tuple[list[int], int]]
) -> Figure:
    sizes: list[int] = []
    actual_ops: list[int] = []
    theoretical_ops: list[int] = []

    d = 4
    k = 10

    for n in range(10, 501, 10):
        arr = [random.randint(0, 9999) for _ in range(n)]
        _, ops = sort_func(arr.copy())

        sizes.append(n)
        actual_ops.append(ops)
        theoretical_ops.append(d * (n + k))

    scale = actual_ops[-1] / theoretical_ops[-1]
    theoretical_scaled: list[float] = [x * scale for x in theoretical_ops]

    fig = Figure(figsize=(9, 6), dpi=100)
    ax = fig.add_subplot(111)

    ax.plot(sizes, actual_ops, marker="o", label="Фактична кількість операцій")
    ax.plot(
        sizes,
        theoretical_scaled,
        linestyle="--",
        label="Теоретична залежність d(n+k)",
    )

    ax.set_xlabel("Розмір масиву n")
    ax.set_ylabel("Кількість операцій")
    ax.set_title("Порівняння фактичної та теоретичної залежностей для Radix Sort")
    ax.grid(True)
    ax.legend()

    fig.tight_layout()
    return fig