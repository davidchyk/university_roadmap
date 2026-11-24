"""Лабораторна робота №7: екстремуми функцій генетичним алгоритмом."""

from __future__ import annotations

from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
SEED = 4106


def function_1d(values: np.ndarray) -> np.ndarray:
    x = values[:, 0]
    return np.sin(np.abs(x)) + np.cos(np.abs(x))


def function_2d(values: np.ndarray) -> np.ndarray:
    x, y = values[:, 0], values[:, 1]
    return x * np.sin(y)


def genetic_optimize(function, bounds, maximize=False, seed=SEED, population_size=10, generations=100):
    rng = np.random.default_rng(seed)
    bounds = np.asarray(bounds, dtype=float)
    dimensions = len(bounds)
    population = rng.uniform(bounds[:, 0], bounds[:, 1], size=(population_size, dimensions))
    best_history, mean_history, diversity_history = [], [], []

    def score(points):
        raw = function(points)
        return raw if maximize else -raw

    for _ in range(generations):
        fitness = score(population)
        elite = population[np.argmax(fitness)].copy()
        raw = function(population)
        best_history.append(float(raw[np.argmax(fitness)]))
        mean_history.append(float(raw.mean()))
        diversity_history.append(float(np.mean(np.std(population, axis=0))))

        children = [elite]
        while len(children) < population_size:
            candidates_a = rng.choice(population_size, 3, replace=False)
            candidates_b = rng.choice(population_size, 3, replace=False)
            parent_a = population[candidates_a[np.argmax(fitness[candidates_a])]]
            parent_b = population[candidates_b[np.argmax(fitness[candidates_b])]]
            alpha = rng.uniform(-0.15, 1.15, dimensions)
            child = alpha * parent_a + (1 - alpha) * parent_b
            mutation_mask = rng.random(dimensions) < 0.20
            scale = (bounds[:, 1] - bounds[:, 0]) * (0.12 * (1 - len(best_history) / generations) + 0.015)
            child += mutation_mask * rng.normal(0, scale)
            children.append(np.clip(child, bounds[:, 0], bounds[:, 1]))
        population = np.asarray(children)

    fitness = score(population)
    best = population[np.argmax(fitness)]
    best_value = float(function(best[None, :])[0])
    return best, best_value, np.asarray(best_history), np.asarray(mean_history), np.asarray(diversity_history)


def main() -> None:
    best_1d, value_1d, hist_1d, mean_1d, div_1d = genetic_optimize(
        function_1d, [(-4, 1)], maximize=False, seed=SEED
    )
    best_2d, value_2d, hist_2d, mean_2d, div_2d = genetic_optimize(
        function_2d, [(-1, 3), (-1, 3)], maximize=True, seed=SEED + 1
    )

    repeated = []
    for run in range(10):
        point_min, result_min, *_ = genetic_optimize(
            function_1d, [(-4, 1)], maximize=False, seed=SEED + 10 + run
        )
        point_max, result_max, *_ = genetic_optimize(
            function_2d, [(-1, 3), (-1, 3)], maximize=True, seed=SEED + 110 + run
        )
        repeated.append((run + 1, point_min[0], result_min, point_max[0], point_max[1], result_max))

    with (RESULTS / "history.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["generation", "best_min", "mean_min", "diversity_min", "best_max", "mean_max", "diversity_max"])
        for i in range(100):
            writer.writerow([i + 1, hist_1d[i], mean_1d[i], div_1d[i], hist_2d[i], mean_2d[i], div_2d[i]])

    with (RESULTS / "repeated_runs.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["run", "minimum_x", "minimum_value", "maximum_x", "maximum_y", "maximum_value"])
        writer.writerows(repeated)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    axes[0].plot(hist_1d, label="Найкраще"); axes[0].plot(mean_1d, label="Середнє", alpha=0.75)
    axes[0].set(title="Мінімізація функції однієї змінної", xlabel="Покоління", ylabel="f(x)")
    axes[1].plot(hist_2d, label="Найкраще"); axes[1].plot(mean_2d, label="Середнє", alpha=0.75)
    axes[1].set(title="Максимізація функції двох змінних", xlabel="Покоління", ylabel="z(x,y)")
    for ax in axes: ax.grid(alpha=0.25); ax.legend()
    fig.tight_layout(); fig.savefig(RESULTS / "convergence.png", dpi=180); plt.close(fig)

    x = np.linspace(-4, 1, 600)
    y = function_1d(x[:, None])
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    ax.plot(x, y)
    ax.scatter(best_1d[0], value_1d, color="crimson", s=65, zorder=5, label=f"ГА: x={best_1d[0]:.4f}")
    ax.set(xlabel="x", ylabel="f(x)", title=r"$f(x)=\sin(|x|)+\cos(|x|)$")
    ax.grid(alpha=0.25); ax.legend()
    fig.tight_layout(); fig.savefig(RESULTS / "minimum_1d.png", dpi=180); plt.close(fig)

    x_axis = np.linspace(-1, 3, 130); y_axis = np.linspace(-1, 3, 130)
    xx, yy = np.meshgrid(x_axis, y_axis)
    zz = xx * np.sin(yy)
    fig = plt.figure(figsize=(8, 5.5)); ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(xx, yy, zz, cmap="viridis", alpha=0.88, linewidth=0)
    ax.scatter(best_2d[0], best_2d[1], value_2d, color="crimson", s=60, label="Результат ГА")
    ax.set(xlabel="x", ylabel="y", zlabel="z", title=r"$z=x\sin(y)$")
    ax.legend(); fig.tight_layout(); fig.savefig(RESULTS / "maximum_2d.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(div_1d, label="1D мінімізація"); ax.plot(div_2d, label="2D максимізація")
    ax.set(xlabel="Покоління", ylabel="Середнє стандартне відхилення", title="Різноманітність популяції")
    ax.grid(alpha=0.25); ax.legend()
    fig.tight_layout(); fig.savefig(RESULTS / "diversity.png", dpi=180); plt.close(fig)

    repeated_array = np.asarray(repeated)
    min_errors = np.abs(repeated_array[:, 2] + np.sqrt(2))
    max_errors = np.abs(repeated_array[:, 5] - 3.0)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0))
    axes[0].semilogy(repeated_array[:, 0], np.maximum(min_errors, 1e-12), marker="o")
    axes[0].set(title="Мінімізація", xlabel="Номер запуску", ylabel="|f - f*|")
    axes[1].semilogy(repeated_array[:, 0], np.maximum(max_errors, 1e-12), marker="o", color="#dd5533")
    axes[1].set(title="Максимізація", xlabel="Номер запуску", ylabel="|z - z*|")
    for ax in axes: ax.grid(alpha=0.25)
    fig.suptitle("Похибка результату в 10 незалежних запусках")
    fig.tight_layout(); fig.savefig(RESULTS / "repeated_runs.png", dpi=180); plt.close(fig)

    min_values = repeated_array[:, 2]
    max_values = repeated_array[:, 5]

    summary = (
        f"Minimum x: {best_1d[0]:.8f}\nMinimum value: {value_1d:.8f}\n"
        f"Maximum x: {best_2d[0]:.8f}\nMaximum y: {best_2d[1]:.8f}\nMaximum value: {value_2d:.8f}\n"
        "Population: 10\nGenerations: 100\nRepeated runs: 10\n"
        f"Repeated minimum mean: {min_values.mean():.10f}\nRepeated minimum std: {min_values.std():.10f}\n"
        f"Repeated maximum mean: {max_values.mean():.10f}\nRepeated maximum std: {max_values.std():.10f}\n"
    )
    (RESULTS / "summary.txt").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
