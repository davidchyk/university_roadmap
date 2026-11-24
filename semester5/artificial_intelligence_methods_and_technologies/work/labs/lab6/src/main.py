"""Лабораторна робота №6: нейро-нечітка TSK-модель температури CPU."""

from __future__ import annotations

from itertools import product
from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
SEED = 4106


def make_dataset(n: int = 650):
    rng = np.random.default_rng(SEED)
    load = rng.uniform(5, 100, n)
    frequency = rng.uniform(1.2, 4.4, n)
    fan = rng.uniform(900, 3600, n)
    temperature = (
        31
        + 0.34 * load
        + 5.3 * (frequency - 2.2)
        - 0.0062 * (fan - 1500)
        + 5.5 * np.sin(np.pi * load / 100) * (frequency - 1.2) / 3.2
        + rng.normal(0, 1.1, n)
    )
    x = np.column_stack([load, frequency, fan])
    return x, temperature


class TSKModel:
    """TSK/ANFIS-подібна мережа з Gaussian premise та лінійними consequent."""

    def __init__(self, inputs: int = 3, membership_functions: int = 2, seed: int = SEED):
        self.inputs = inputs
        self.mf = membership_functions
        self.rules = np.asarray(list(product(range(self.mf), repeat=self.inputs)), dtype=int)
        self.rng = np.random.default_rng(seed)
        self.centers = np.tile(np.linspace(-0.65, 0.65, self.mf), (inputs, 1))
        self.sigmas = np.full((inputs, self.mf), 0.75)
        self.theta = np.zeros((len(self.rules), inputs + 1))

    def _weights(self, x: np.ndarray, centers=None, sigmas=None) -> np.ndarray:
        centers = self.centers if centers is None else centers
        sigmas = self.sigmas if sigmas is None else sigmas
        degrees = np.empty((len(x), self.inputs, self.mf))
        for j in range(self.inputs):
            for k in range(self.mf):
                degrees[:, j, k] = np.exp(-0.5 * ((x[:, j] - centers[j, k]) / sigmas[j, k]) ** 2)
        firing = np.ones((len(x), len(self.rules)))
        for r, rule in enumerate(self.rules):
            for j, mf_index in enumerate(rule):
                firing[:, r] *= degrees[:, j, mf_index]
        return firing / (firing.sum(axis=1, keepdims=True) + 1e-12)

    def _design(self, x: np.ndarray, centers=None, sigmas=None) -> np.ndarray:
        weights = self._weights(x, centers, sigmas)
        augmented = np.column_stack([np.ones(len(x)), x])
        return (weights[:, :, None] * augmented[:, None, :]).reshape(len(x), -1)

    def fit_consequents(self, x: np.ndarray, y: np.ndarray, ridge: float = 1e-4, centers=None, sigmas=None):
        phi = self._design(x, centers, sigmas)
        regularizer = ridge * np.eye(phi.shape[1])
        theta = np.linalg.solve(phi.T @ phi + regularizer, phi.T @ y)
        return theta.reshape(len(self.rules), self.inputs + 1)

    def predict(self, x: np.ndarray, centers=None, sigmas=None, theta=None) -> np.ndarray:
        theta = self.theta if theta is None else theta
        return self._design(x, centers, sigmas) @ theta.ravel()

    def fit(self, x_train, y_train, x_val, y_val, epochs: int = 35):
        self.theta = self.fit_consequents(x_train, y_train)
        best = np.mean((self.predict(x_val) - y_val) ** 2)
        history = [best]
        step_center, step_sigma = 0.10, 0.07
        for _ in range(epochs - 1):
            candidate_centers = self.centers + self.rng.normal(0, step_center, self.centers.shape)
            candidate_centers.sort(axis=1)
            candidate_sigmas = np.clip(
                self.sigmas + self.rng.normal(0, step_sigma, self.sigmas.shape), 0.28, 1.4
            )
            candidate_theta = self.fit_consequents(
                x_train, y_train, centers=candidate_centers, sigmas=candidate_sigmas
            )
            prediction = self.predict(
                x_val, centers=candidate_centers, sigmas=candidate_sigmas, theta=candidate_theta
            )
            mse = np.mean((prediction - y_val) ** 2)
            if mse < best:
                self.centers, self.sigmas, self.theta = candidate_centers, candidate_sigmas, candidate_theta
                best = mse
            history.append(best)
            step_center *= 0.95
            step_sigma *= 0.95
        return history


def metrics(y: np.ndarray, pred: np.ndarray):
    rmse = float(np.sqrt(np.mean((y - pred) ** 2)))
    mae = float(np.mean(np.abs(y - pred)))
    r2 = float(1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2))
    return rmse, mae, r2


def plot_architecture(path: Path) -> None:
    """Візуалізує п'ять функціональних шарів TSK/ANFIS."""
    layers = [
        ("Входи", 3, "x₁, x₂, x₃"),
        ("Фазифікація", 6, "Gaussian MF"),
        ("Правила", 8, "w₁…w₈"),
        ("Нормалізація", 8, "w̄₁…w̄₈"),
        ("TSK-наслідки", 8, "w̄ₖfₖ"),
        ("Вихід", 1, "Σw̄ₖfₖ"),
    ]
    fig, ax = plt.subplots(figsize=(11, 4.2))
    x_positions = np.arange(len(layers))
    for index, (title, count, subtitle) in enumerate(layers):
        height = min(count, 8)
        y_positions = np.linspace(-1, 1, height)
        ax.scatter(np.full(height, index), y_positions, s=180, color="#4c78a8", edgecolor="white", zorder=3)
        ax.text(index, 1.42, title, ha="center", va="bottom", fontweight="bold")
        ax.text(index, -1.42, f"{count} вузл.\n{subtitle}", ha="center", va="top", fontsize=9)
        if index < len(layers) - 1:
            ax.annotate("", xy=(index + 0.78, 0), xytext=(index + 0.22, 0), arrowprops=dict(arrowstyle="->", lw=1.6))
    ax.set_xlim(-0.6, len(layers) - 0.4); ax.set_ylim(-1.9, 1.9)
    ax.axis("off"); ax.set_title("Структура гібридної нейро-нечіткої мережі TSK", pad=16)
    fig.tight_layout(); fig.savefig(path, dpi=180); plt.close(fig)


def main() -> None:
    x, y = make_dataset()
    rng = np.random.default_rng(SEED)
    order = rng.permutation(len(x))
    train_idx, test_idx = order[:520], order[520:]
    x_train_raw, x_test_raw = x[train_idx], x[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    x_mean, x_std = x_train_raw.mean(axis=0), x_train_raw.std(axis=0)
    x_train = (x_train_raw - x_mean) / x_std
    x_test = (x_test_raw - x_mean) / x_std

    # Частину навчальної вибірки використовуємо для контролю premise-параметрів.
    split = 430
    model = TSKModel()
    history = model.fit(x_train[:split], y_train[:split], x_train[split:], y_train[split:])
    model.theta = model.fit_consequents(x_train, y_train)
    train_pred = model.predict(x_train)
    test_pred = model.predict(x_test)
    train_metrics = metrics(y_train, train_pred)
    test_metrics = metrics(y_test, test_pred)
    plot_architecture(RESULTS / "architecture.png")

    with (RESULTS / "predictions.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["load", "frequency", "fan", "actual_temperature", "predicted_temperature"])
        for row, actual, predicted in zip(x_test_raw, y_test, test_pred):
            writer.writerow([*row, actual, predicted])

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(np.arange(1, len(history) + 1), history, marker="o", markersize=3)
    ax.set(xlabel="Епоха", ylabel="Validation MSE", title="Навчання нейро-нечіткої мережі")
    ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(RESULTS / "training.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    ax.scatter(y_test, test_pred, alpha=0.7, s=24)
    limits = [min(y_test.min(), test_pred.min()), max(y_test.max(), test_pred.max())]
    ax.plot(limits, limits, "k--", label="Ідеальний прогноз")
    ax.set(xlabel="Фактична температура, °C", ylabel="Прогноз, °C", title="Перевірка адекватності моделі")
    ax.legend(); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(RESULTS / "prediction.png", dpi=180); plt.close(fig)

    names = ["Завантаження CPU", "Частота", "Швидкість вентилятора"]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
    grid = np.linspace(-2.2, 2.2, 300)
    for j, ax in enumerate(axes):
        for k in range(model.mf):
            degree = np.exp(-0.5 * ((grid - model.centers[j, k]) / model.sigmas[j, k]) ** 2)
            ax.plot(grid, degree, label=f"MF{k + 1}")
        ax.set(title=names[j], xlabel="Нормоване значення", ylabel="μ")
        ax.grid(alpha=0.2); ax.legend()
    fig.tight_layout(); fig.savefig(RESULTS / "membership_functions.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 4.2))
    sample = np.argsort(y_test)[:60]
    ax.plot(y_test[sample], label="Фактична", marker="o", markersize=3)
    ax.plot(test_pred[sample], label="Прогноз", marker="x", markersize=3)
    ax.set(xlabel="Тестовий приклад (впорядковано)", ylabel="Температура, °C", title="Фактичні та прогнозовані значення")
    ax.legend(); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(RESULTS / "comparison.png", dpi=180); plt.close(fig)

    summary = (
        f"Samples: {len(x)}\nRules: {len(model.rules)}\nEpochs: {len(history)}\n"
        f"Train RMSE: {train_metrics[0]:.6f}\nTrain MAE: {train_metrics[1]:.6f}\nTrain R2: {train_metrics[2]:.6f}\n"
        f"Test RMSE: {test_metrics[0]:.6f}\nTest MAE: {test_metrics[1]:.6f}\nTest R2: {test_metrics[2]:.6f}\n"
    )
    (RESULTS / "summary.txt").write_text(summary, encoding="utf-8")
    np.savetxt(RESULTS / "centers.csv", model.centers, delimiter=",")
    np.savetxt(RESULTS / "sigmas.csv", model.sigmas, delimiter=",")
    print(summary)


if __name__ == "__main__":
    main()
