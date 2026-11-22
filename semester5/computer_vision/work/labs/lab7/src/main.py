from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
RESULTS = PROJECT / "results"
RNG = np.random.default_rng(4106)

SIZE = 16
CLASSES = ["plus", "cross", "square", "triangle", "circle", "arrow"]
HIDDEN = 64
EPOCHS = 180
LEARNING_RATE = 0.12
BATCH_SIZE = 64


def template(kind: str) -> np.ndarray:
    image = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(image)
    if kind == "plus":
        draw.rectangle((6, 2, 9, 13), fill=255)
        draw.rectangle((2, 6, 13, 9), fill=255)
    elif kind == "cross":
        draw.line((3, 3, 12, 12), fill=255, width=3)
        draw.line((12, 3, 3, 12), fill=255, width=3)
    elif kind == "square":
        draw.rectangle((3, 3, 12, 12), outline=255, width=3)
    elif kind == "triangle":
        draw.polygon([(8, 2), (2, 13), (13, 13)], outline=255)
        draw.line((8, 2, 2, 13), fill=255, width=3)
        draw.line((2, 13, 13, 13), fill=255, width=3)
        draw.line((13, 13, 8, 2), fill=255, width=3)
    elif kind == "circle":
        draw.ellipse((2, 2, 13, 13), outline=255, width=3)
    elif kind == "arrow":
        draw.rectangle((2, 6, 9, 9), fill=255)
        draw.polygon([(8, 2), (14, 8), (8, 13)], fill=255)
    return np.asarray(image, dtype=np.float64) / 255.0


def augment(base: np.ndarray, count: int) -> np.ndarray:
    result = []
    for _ in range(count):
        dy, dx = RNG.integers(-2, 3, size=2)
        shifted = np.roll(base, (dy, dx), axis=(0, 1))
        if dy > 0:
            shifted[:dy] = 0
        elif dy < 0:
            shifted[dy:] = 0
        if dx > 0:
            shifted[:, :dx] = 0
        elif dx < 0:
            shifted[:, dx:] = 0
        noisy = np.clip(shifted + RNG.normal(0, 0.10, shifted.shape), 0, 1)
        if RNG.random() < 0.45:
            flips = RNG.random(shifted.shape) < 0.015
            noisy[flips] = 1 - noisy[flips]
        result.append(noisy)
    return np.asarray(result)


def make_dataset(per_class: int = 320) -> tuple[np.ndarray, np.ndarray]:
    samples, labels = [], []
    for class_index, name in enumerate(CLASSES):
        batch = augment(template(name), per_class)
        samples.append(batch.reshape(per_class, -1))
        labels.extend([class_index] * per_class)
    x = np.vstack(samples)
    y = np.asarray(labels, dtype=np.int64)
    order = RNG.permutation(len(x))
    return x[order], y[order]


def softmax(values: np.ndarray) -> np.ndarray:
    shifted = values - values.max(axis=1, keepdims=True)
    exponent = np.exp(shifted)
    return exponent / exponent.sum(axis=1, keepdims=True)


class NeuralNetwork:
    """Одношарова MLP, навчання якої реалізовано матричними операціями NumPy."""

    def __init__(self) -> None:
        self.w1 = RNG.normal(0, np.sqrt(2 / (SIZE * SIZE)), (SIZE * SIZE, HIDDEN))
        self.b1 = np.zeros((1, HIDDEN))
        self.w2 = RNG.normal(0, np.sqrt(2 / HIDDEN), (HIDDEN, len(CLASSES)))
        self.b2 = np.zeros((1, len(CLASSES)))

    def forward(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        hidden = np.maximum(0, x @ self.w1 + self.b1)
        return hidden, softmax(hidden @ self.w2 + self.b2)

    def train_batch(self, x: np.ndarray, y: np.ndarray) -> float:
        hidden, probabilities = self.forward(x)
        target = np.eye(len(CLASSES))[y]
        loss = -np.log(probabilities[np.arange(len(y)), y] + 1e-12).mean()

        gradient_output = (probabilities - target) / len(x)
        gradient_w2 = hidden.T @ gradient_output
        gradient_b2 = gradient_output.sum(axis=0, keepdims=True)
        gradient_hidden = gradient_output @ self.w2.T
        gradient_hidden[hidden <= 0] = 0
        gradient_w1 = x.T @ gradient_hidden
        gradient_b1 = gradient_hidden.sum(axis=0, keepdims=True)

        self.w2 -= LEARNING_RATE * gradient_w2
        self.b2 -= LEARNING_RATE * gradient_b2
        self.w1 -= LEARNING_RATE * gradient_w1
        self.b1 -= LEARNING_RATE * gradient_b1
        return float(loss)

    def predict(self, x: np.ndarray) -> np.ndarray:
        return self.forward(x)[1].argmax(axis=1)


def confusion_matrix(actual: np.ndarray, predicted: np.ndarray) -> np.ndarray:
    matrix = np.zeros((len(CLASSES), len(CLASSES)), dtype=int)
    for y, p in zip(actual, predicted):
        matrix[y, p] += 1
    return matrix


def save_visuals(
    losses: list[float], matrix: np.ndarray, examples: np.ndarray, predictions: np.ndarray
) -> None:
    fig, axes = plt.subplots(1, len(CLASSES), figsize=(12, 2.4))
    for axis, name in zip(axes, CLASSES):
        axis.imshow(template(name), cmap="gray", vmin=0, vmax=1)
        axis.set_title(name)
        axis.axis("off")
    fig.suptitle("Шість еталонних спеціальних знаків")
    fig.tight_layout()
    fig.savefig(RESULTS / "templates.png", dpi=180)
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(8, 4))
    axis.plot(losses, color="navy")
    axis.set(xlabel="Епоха", ylabel="Cross-entropy", title="Процес навчання нейромережі")
    axis.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(RESULTS / "training_curve.png", dpi=180)
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(6, 5))
    image = axis.imshow(matrix, cmap="Blues")
    axis.set_xticks(range(len(CLASSES)), CLASSES, rotation=35, ha="right")
    axis.set_yticks(range(len(CLASSES)), CLASSES)
    axis.set(xlabel="Передбачений клас", ylabel="Справжній клас", title="Матриця помилок")
    for y in range(len(CLASSES)):
        for x in range(len(CLASSES)):
            axis.text(x, y, matrix[y, x], ha="center", va="center")
    fig.colorbar(image, ax=axis, shrink=0.8)
    fig.tight_layout()
    fig.savefig(RESULTS / "confusion_matrix.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(2, 6, figsize=(12, 4.5))
    for axis, sample, prediction in zip(axes.ravel(), examples[:12], predictions[:12]):
        axis.imshow(sample.reshape(SIZE, SIZE), cmap="gray", vmin=0, vmax=1)
        axis.set_title(CLASSES[prediction], fontsize=9)
        axis.axis("off")
    fig.suptitle("Розпізнавання зашумлених і зміщених знаків")
    fig.tight_layout()
    fig.savefig(RESULTS / "predictions.png", dpi=180)
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    x, y = make_dataset()
    split = int(0.8 * len(x))
    x_train, x_test = x[:split], x[split:]
    y_train, y_test = y[:split], y[split:]

    network = NeuralNetwork()
    losses: list[float] = []
    for epoch in range(EPOCHS):
        order = RNG.permutation(len(x_train))
        batch_losses = []
        for start in range(0, len(order), BATCH_SIZE):
            indices = order[start : start + BATCH_SIZE]
            batch_losses.append(network.train_batch(x_train[indices], y_train[indices]))
        losses.append(float(np.mean(batch_losses)))

    predicted = network.predict(x_test)
    matrix = confusion_matrix(y_test, predicted)
    accuracy = float((predicted == y_test).mean())
    save_visuals(losses, matrix, x_test, predicted)

    np.savez_compressed(
        RESULTS / "model.npz",
        w1=network.w1,
        b1=network.b1,
        w2=network.w2,
        b2=network.b2,
        classes=np.asarray(CLASSES),
    )
    with (RESULTS / "metrics.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["metric", "value"])
        writer.writerow(["train_samples", len(x_train)])
        writer.writerow(["test_samples", len(x_test)])
        writer.writerow(["epochs", EPOCHS])
        writer.writerow(["accuracy", f"{accuracy:.6f}"])
        writer.writerow(["final_loss", f"{losses[-1]:.6f}"])

    print(f"Точність на тестовій вибірці: {accuracy:.4%}")
    print(f"Фінальна cross-entropy: {losses[-1]:.6f}")
    print("Результати:", RESULTS)


if __name__ == "__main__":
    main()
