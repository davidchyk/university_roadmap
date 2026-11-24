"""Run the complete fixed-architecture experiment for variant 52."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import time

import matplotlib.pyplot as plt
import numpy as np

from mkr_core import (
    AdamConfig,
    FeedForwardNetwork,
    GAConfig,
    error_metrics,
    make_grid,
    split_dataset,
    target_function,
    train_adam,
    train_genetic,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
ARCHITECTURE = (2, 4, 8, 10, 6, 6, 1)
SEED = 4106


def plot_surfaces(xx, yy, exact, predicted, error):
    items = [
        (exact, "Точна поверхня функції", "target_surface.png", "viridis"),
        (predicted, "Прогноз нейромережі після навчання ГА", "prediction_surface.png", "viridis"),
        (error, "Абсолютна похибка", "error_surface.png", "magma"),
    ]
    for values, title, filename, cmap in items:
        figure = plt.figure(figsize=(8.3, 5.4))
        axes = figure.add_subplot(111, projection="3d")
        axes.plot_surface(xx, yy, values, cmap=cmap, linewidth=0, antialiased=True)
        axes.set(xlabel="x", ylabel="y", zlabel="z" if "похибка" not in title.lower() else "|e|")
        axes.set_title(title)
        figure.tight_layout()
        figure.savefig(RESULTS / filename, dpi=190)
        plt.close(figure)


def main() -> None:
    inputs, targets, xx, yy = make_grid(points=31)
    x_train, y_train, x_test, y_test = split_dataset(inputs, targets, seed=SEED)
    network = FeedForwardNetwork(ARCHITECTURE)
    ga_config = GAConfig(population_size=80, generations=280, seed=SEED, patience=90)

    started = time.perf_counter()
    random_ga = train_genetic(network, x_train, y_train, ga_config, initialization="random")
    random_seconds = time.perf_counter() - started

    started = time.perf_counter()
    nw_ga = train_genetic(
        network,
        x_train,
        y_train,
        GAConfig(**{**ga_config.__dict__, "seed": SEED + 1}),
        initialization="nguyen_widrow",
    )
    nw_seconds = time.perf_counter() - started

    started = time.perf_counter()
    adam = train_adam(network, x_train, y_train, AdamConfig(epochs=1200, seed=SEED + 2))
    adam_seconds = time.perf_counter() - started

    methods = {
        "GA random": (random_ga["chromosome"], random_seconds, random_ga["generations_completed"]),
        "GA Nguyen-Widrow": (nw_ga["chromosome"], nw_seconds, nw_ga["generations_completed"]),
        "Adam backprop": (adam["chromosome"], adam_seconds, adam["epochs_completed"]),
    }
    metrics = {}
    for name, (chromosome, seconds, iterations) in methods.items():
        metrics[name] = {
            "train": error_metrics(y_train, network.forward(x_train, chromosome)),
            "test": error_metrics(y_test, network.forward(x_test, chromosome)),
            "seconds": seconds,
            "iterations": iterations,
        }

    full_prediction = network.forward(inputs, nw_ga["chromosome"]).reshape(xx.shape)
    exact_surface = targets.reshape(xx.shape)
    absolute_error = np.abs(full_prediction - exact_surface)
    plot_surfaces(xx, yy, exact_surface, full_prediction, absolute_error)

    figure, axes = plt.subplots(1, 2, figsize=(11, 4.3))
    axes[0].semilogy(random_ga["best_history"], label="ГА: випадкова ініціалізація")
    axes[0].semilogy(nw_ga["best_history"], label="ГА: Нгуєн-Відроу")
    axes[0].set(xlabel="Покоління", ylabel="Найкраща MSE", title="Збіжність генетичного алгоритму")
    axes[1].semilogy(adam["history"], color="#d95f02", label="Adam")
    axes[1].set(xlabel="Епоха", ylabel="MSE", title="Навчання методом backpropagation")
    for axes_item in axes:
        axes_item.grid(alpha=0.25)
        axes_item.legend()
    figure.tight_layout()
    figure.savefig(RESULTS / "convergence.png", dpi=190)
    plt.close(figure)

    labels = list(metrics)
    test_mse = [metrics[name]["test"]["mse"] for name in labels]
    figure, axes = plt.subplots(figsize=(8, 4.5))
    bars = axes.bar(labels, test_mse, color=["#4c78a8", "#59a14f", "#f28e2b"])
    axes.set_yscale("log")
    axes.set(ylabel="Тестова MSE (логарифмічна шкала)", title="Порівняння методів навчання")
    axes.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, test_mse):
        axes.text(bar.get_x() + bar.get_width() / 2, value * 1.12, f"{value:.2e}", ha="center")
    figure.tight_layout()
    figure.savefig(RESULTS / "method_comparison.png", dpi=190)
    plt.close(figure)

    slice_x = np.linspace(0, 1, 250)
    slice_y = np.full_like(slice_x, 0.5)
    slice_inputs = np.column_stack([slice_x, slice_y])
    figure, axes = plt.subplots(figsize=(8.2, 4.4))
    axes.plot(slice_x, target_function(slice_x, slice_y), label="Точна функція", linewidth=2.2)
    axes.plot(slice_x, network.forward(slice_inputs, nw_ga["chromosome"]).ravel(), "--", label="Прогноз ГА")
    axes.set(xlabel="x при y=0,5", ylabel="z", title="Контрольний переріз поверхні")
    axes.grid(alpha=0.25)
    axes.legend()
    figure.tight_layout()
    figure.savefig(RESULTS / "slice_comparison.png", dpi=190)
    plt.close(figure)

    serializable = {
        "architecture": list(ARCHITECTURE),
        "parameters": network.parameter_count,
        "interval": {"x": [0, 1], "y": [0, 1]},
        "grid_points": 31,
        "train_samples": len(x_train),
        "test_samples": len(x_test),
        "feature_significance": nw_ga["feature_significance"].tolist(),
        "methods": metrics,
    }
    (RESULTS / "metrics.json").write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")
    with (RESULTS / "comparison.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["method", "train_mse", "test_mse", "test_rmse", "test_mae", "test_max_abs", "iterations", "seconds"])
        for name in labels:
            row = metrics[name]
            writer.writerow([
                name,
                row["train"]["mse"],
                row["test"]["mse"],
                row["test"]["rmse"],
                row["test"]["mae"],
                row["test"]["max_abs"],
                row["iterations"],
                row["seconds"],
            ])
    np.savez_compressed(
        RESULTS / "trained_models.npz",
        random_ga=random_ga["chromosome"],
        nguyen_widrow_ga=nw_ga["chromosome"],
        adam=adam["chromosome"],
        architecture=np.asarray(ARCHITECTURE),
    )
    print(json.dumps(serializable, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
