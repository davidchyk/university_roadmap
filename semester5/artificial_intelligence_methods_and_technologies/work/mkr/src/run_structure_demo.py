"""Headless demonstration of the GUI's structural synthesis engine."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

from mkr_core import make_grid, split_dataset
from structure_search import StructureConfig, search_architecture


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def main() -> None:
    inputs, targets, _, _ = make_grid(points=13)
    x_train, y_train, x_test, y_test = split_dataset(inputs, targets, seed=4106)
    config = StructureConfig(
        max_total_neurons=24,
        population_size=7,
        generations=6,
        inner_population=18,
        inner_generations=30,
        target_mse=0.001,
    )
    result = search_architecture(x_train, y_train, x_test, y_test, config)
    data = {
        "architecture": list(result["architecture"]),
        "validation_mse": result["mse"],
        "generations": len(result["history"]),
        "evaluated_architectures": len(result["candidates"]),
        "history": result["history"].tolist(),
        "candidates": [
            {**item, "architecture": list(item["architecture"])} for item in result["candidates"]
        ],
    }
    (RESULTS / "structure_search.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    figure, axes = plt.subplots(figsize=(7.5, 4.2))
    axes.semilogy(range(1, len(result["history"]) + 1), result["history"], marker="o")
    axes.set(xlabel="Покоління структурного ГА", ylabel="Валідаційна MSE", title="Структурний синтез мережі")
    axes.grid(alpha=0.25)
    figure.tight_layout()
    figure.savefig(RESULTS / "structure_search.png", dpi=190)
    plt.close(figure)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
