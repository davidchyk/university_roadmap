from __future__ import annotations

from matplotlib.figure import Figure

from src.aitken import interpolate_full


def build_interpolation_figure(
    func,
    x_nodes: list[float],
    y_nodes: list[float],
    a: float,
    b: float,
    x_value: float,
    plot_points: int,
) -> Figure:
    x_dense = [a + (b - a) * i / (plot_points - 1) for i in range(plot_points)]
    y_true = [func(x) for x in x_dense]
    y_interp = [interpolate_full(x_nodes, y_nodes, x) for x in x_dense]
    y_error = [abs(y1 - y2) for y1, y2 in zip(y_true, y_interp)]

    true_at_x = func(x_value)
    interp_at_x = interpolate_full(x_nodes, y_nodes, x_value)

    fig = Figure(figsize=(8.2, 5.8), dpi=100)
    ax = fig.add_subplot(111)

    ax.plot(x_dense, y_true, label="f(x)")
    ax.plot(x_dense, y_interp, label="Aitken interpolation")
    ax.plot(x_dense, y_error, label="|f(x)-P(x)|")
    ax.scatter(x_nodes, y_nodes, label="Nodes")
    ax.scatter([x_value], [true_at_x], label="f(x*)")
    ax.scatter([x_value], [interp_at_x], label="P(x*)")

    ax.set_title("Aitken interpolation graph")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()

    return fig