"""Лабораторна робота №2: нечітке моделювання функції двох змінних.

Варіант 6:
    y = sin(|x|) + cos(|x|)
    z = x * sin(y)
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


N_INPUT = 6
N_OUTPUT = 9
GRID_STEP = 0.02
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "results"


def auxiliary_y(x: np.ndarray) -> np.ndarray:
    return np.sin(np.abs(x)) + np.cos(np.abs(x))


def target_z(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return x * np.sin(y)


def triangular(x: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
    result = np.zeros_like(x, dtype=float)
    if b > a:
        result = np.maximum(result, np.where((x > a) & (x <= b), (x - a) / (b - a), 0.0))
    if c > b:
        result = np.maximum(result, np.where((x > b) & (x < c), (c - x) / (c - b), 0.0))
    result = np.maximum(result, np.where(x == b, 1.0, 0.0))
    return np.clip(result, 0.0, 1.0)


def trapezoidal(x: np.ndarray, a: float, b: float, c: float, d: float) -> np.ndarray:
    result = np.zeros_like(x, dtype=float)
    if b > a:
        result = np.maximum(result, np.where((x > a) & (x < b), (x - a) / (b - a), 0.0))
    result = np.maximum(result, np.where((x >= b) & (x <= c), 1.0, 0.0))
    if d > c:
        result = np.maximum(result, np.where((x > c) & (x < d), (d - x) / (d - c), 0.0))
    return np.clip(result, 0.0, 1.0)


def gaussian(x: np.ndarray, center: float, sigma: float) -> np.ndarray:
    return np.exp(-0.5 * ((x - center) / sigma) ** 2)


def make_memberships(domain: np.ndarray, centers: np.ndarray, kind: str) -> np.ndarray:
    step = centers[1] - centers[0]
    functions = []
    for index, center in enumerate(centers):
        if kind == "triangular":
            if index == 0:
                values = trapezoidal(domain, centers[0], centers[0], centers[1], centers[2])
            elif index == len(centers) - 1:
                values = trapezoidal(domain, centers[-3], centers[-2], centers[-1], centers[-1])
            else:
                values = triangular(domain, centers[index - 1], center, centers[index + 1])
        elif kind == "trapezoidal":
            values = trapezoidal(domain, center - step * 0.65, center - step * 0.25,
                                 center + step * 0.25, center + step * 0.65)
        elif kind == "gaussian":
            values = gaussian(domain, center, step * 0.55)
        else:
            raise ValueError(f"Невідомий тип функцій: {kind}")
        functions.append(values)
    return np.asarray(functions)


def build_rules(x_centers: np.ndarray, y_centers: np.ndarray, output_centers: np.ndarray) -> np.ndarray:
    rules = np.empty((len(x_centers), len(y_centers)), dtype=int)
    for i, x_value in enumerate(x_centers):
        for j, y_value in enumerate(y_centers):
            value = float(target_z(np.array(x_value), np.array(y_value)))
            rules[i, j] = int(np.argmin(np.abs(output_centers - value)))
    return rules


def infer(x_values: np.ndarray, y_values: np.ndarray, x_centers: np.ndarray,
          y_centers: np.ndarray, output_grid: np.ndarray, output_centers: np.ndarray,
          kind: str, rules: np.ndarray, diagonal_only: bool = False) -> np.ndarray:
    """Mamdani: min для AND, max для агрегації, centroid для дефазифікації."""
    x_membership = make_memberships(x_values, x_centers, kind)
    y_membership = make_memberships(y_values, y_centers, kind)
    output_membership = make_memberships(output_grid, output_centers, kind)
    result = np.empty((len(y_values), len(x_values)), dtype=float)

    for row, y_members in enumerate(y_membership.T):
        for column, x_members in enumerate(x_membership.T):
            aggregated = np.zeros_like(output_grid, dtype=float)
            for i in range(N_INPUT):
                for j in range(N_INPUT):
                    if diagonal_only and i != j:
                        continue
                    activation = min(x_members[i], y_members[j])
                    aggregated = np.maximum(aggregated,
                                            np.minimum(activation, output_membership[rules[i, j]]))
            denominator = np.trapezoid(aggregated, output_grid)
            result[row, column] = (np.trapezoid(output_grid * aggregated, output_grid) / denominator
                                   if denominator > 1e-12 else output_centers[0])
    return result


def relative_error(exact: np.ndarray, predicted: np.ndarray) -> np.ndarray:
    return np.abs((exact + 1.0) - (predicted + 1.0)) / np.abs(exact + 1.0) * 100.0


def save_membership_plot(kind: str, domain: np.ndarray, centers: np.ndarray,
                         title: str, path: Path) -> None:
    plt.figure(figsize=(10, 5))
    for index, values in enumerate(make_memberships(domain, centers, kind), start=1):
        plt.plot(domain, values, label=f"m{index}")
    plt.title(title)
    plt.xlabel("Значення змінної")
    plt.ylabel("Ступінь належності")
    plt.ylim(-0.02, 1.05)
    plt.grid(alpha=0.3)
    plt.legend(ncol=3)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def save_surface(x: np.ndarray, y: np.ndarray, values: np.ndarray,
                 title: str, path: Path) -> None:
    figure = plt.figure(figsize=(9, 6))
    axes = figure.add_subplot(111, projection="3d")
    xx, yy = np.meshgrid(x, y)
    axes.plot_surface(xx, yy, values, cmap="viridis", linewidth=0, antialiased=True)
    axes.set_xlabel("x")
    axes.set_ylabel("y")
    axes.set_zlabel("z")
    axes.set_title(title)
    figure.tight_layout()
    figure.savefig(path, dpi=180)
    plt.close(figure)


def save_rules(rules: np.ndarray, path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["y \\ x"] + [f"mx{i}" for i in range(1, N_INPUT + 1)])
        for j in range(N_INPUT):
            writer.writerow([f"my{j + 1}"] + [f"mf{rules[i, j] + 1}" for i in range(N_INPUT)])


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Нормалізований діапазон x; y беремо з першої формули варіанта.
    x_values = np.arange(0.0, 1.0 + GRID_STEP / 2, GRID_STEP)
    y_values = np.linspace(1.0, float(auxiliary_y(np.array(1.0))), len(x_values))
    x_centers = np.linspace(x_values.min(), x_values.max(), N_INPUT)
    y_centers = np.linspace(y_values.min(), y_values.max(), N_INPUT)

    xx, yy = np.meshgrid(x_values, y_values)
    exact = target_z(xx, yy)
    z_min = min(0.0, float(exact.min()))
    z_max = max(float(exact.max()), 0.01)
    output_centers = np.linspace(z_min, z_max, N_OUTPUT)
    output_grid = np.linspace(z_min, z_max, 501)

    results = []
    rules = build_rules(x_centers, y_centers, output_centers)
    save_rules(rules, OUTPUT_DIR / "rules.csv")
    for kind in ("triangular", "trapezoidal", "gaussian"):
        predicted = infer(x_values, y_values, x_centers, y_centers, output_grid,
                          output_centers, kind, rules)
        diagonal = infer(x_values, y_values, x_centers, y_centers, output_grid,
                         output_centers, kind, rules, diagonal_only=True)
        error = relative_error(exact, predicted)
        diagonal_error = relative_error(exact, diagonal)
        results.append((kind, error.mean(), error.max(), diagonal_error.mean()))

        save_membership_plot(kind, x_values, x_centers, f"Функції належності x ({kind})",
                             OUTPUT_DIR / f"memberships_x_{kind}.png")
        save_membership_plot(kind, y_values, y_centers, f"Функції належності y ({kind})",
                             OUTPUT_DIR / f"memberships_y_{kind}.png")
        save_membership_plot(kind, output_grid, output_centers, f"Функції належності z ({kind})",
                             OUTPUT_DIR / f"memberships_z_{kind}.png")
        save_surface(x_values, y_values, predicted, f"Нечітка модель ({kind})",
                     OUTPUT_DIR / f"surface_{kind}.png")
        save_surface(x_values, y_values, np.abs(exact - predicted), f"Абсолютна похибка ({kind})",
                     OUTPUT_DIR / f"error_{kind}.png")

    with (OUTPUT_DIR / "results.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Тип", "Середня похибка, %", "Максимальна похибка, %",
                         "Середня похибка лише діагоналі, %"])
        writer.writerows(results)

    print(f"Результати збережено у: {OUTPUT_DIR}")
    print("Тип          Середня, %    Максимальна, %    Лише діагональ, %")
    for kind, mean_error, max_error, diagonal_mean in results:
        print(f"{kind:12} {mean_error:12.4f} {max_error:17.4f} {diagonal_mean:20.4f}")


if __name__ == "__main__":
    main()
