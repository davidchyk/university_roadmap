"""Лабораторна робота №5: компактна CNN для розпізнавання цифр.

Програма не потребує TensorFlow/PyTorch. Вона генерує локальний набір
28x28-зображень цифр у форматі, сумісному з MNIST, і навчає згорткову
мережу засобами NumPy. Якщо потрібно працювати саме з оригінальним MNIST,
функцію generate_digit_dataset можна замінити завантаженням mnist.npz.
"""

from __future__ import annotations

from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
DATA = ROOT / "data" / "mnist.npz"
RESULTS.mkdir(parents=True, exist_ok=True)
SEED = 4106


def _font_paths() -> list[str]:
    candidates = [
        "/usr/share/fonts/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/noto/NotoSans-Bold.ttf",
        "/usr/share/fonts/noto/NotoSerif-Regular.ttf",
        "/usr/share/fonts/noto/NotoSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
    ]
    available = [path for path in candidates if Path(path).exists()]
    if not available:
        raise FileNotFoundError("Не знайдено системного шрифту для генерації цифр")
    return available


def render_digit(label: int, rng: np.random.Generator, noisy: bool) -> np.ndarray:
    """Створює варіативне 28x28-зображення цифри."""
    canvas = Image.new("L", (36, 36), color=0)
    draw = ImageDraw.Draw(canvas)
    font_path = rng.choice(_font_paths())
    font_size = int(rng.integers(23, 31))
    font = ImageFont.truetype(font_path, font_size)
    text = str(label)
    bbox = draw.textbbox((0, 0), text, font=font)
    width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    shift_x = int(rng.integers(-3, 4))
    shift_y = int(rng.integers(-3, 4))
    x = (36 - width) // 2 - bbox[0] + shift_x
    y = (36 - height) // 2 - bbox[1] + shift_y
    draw.text((x, y), text, fill=255, font=font)

    angle = float(rng.uniform(-13, 13))
    canvas = canvas.rotate(angle, resample=Image.Resampling.BILINEAR, fillcolor=0)
    canvas = canvas.crop((4, 4, 32, 32))
    if noisy:
        canvas = canvas.filter(ImageFilter.GaussianBlur(radius=float(rng.uniform(0.3, 0.9))))

    array = np.asarray(canvas, dtype=np.float32) / 255.0
    noise_std = 0.075 if noisy else 0.035
    array = np.clip(array + rng.normal(0.0, noise_std, array.shape), 0.0, 1.0)
    if noisy and rng.random() < 0.20:
        # Часткове стирання імітує дефект написання.
        row = int(rng.integers(7, 21))
        array[row : row + 2, int(rng.integers(4, 10)) : int(rng.integers(18, 25))] *= 0.2
    return array


def generate_digit_dataset(
    train_per_class: int = 150, test_per_class: int = 30
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(SEED)
    if DATA.exists():
        with np.load(DATA) as dataset:
            full_x_train = dataset["x_train"]
            full_y_train = dataset["y_train"]
            full_x_test = dataset["x_test"]
            full_y_test = dataset["y_test"]
        train_indices, test_indices = [], []
        for label in range(10):
            train_indices.extend(rng.choice(np.flatnonzero(full_y_train == label), train_per_class, replace=False))
            test_indices.extend(rng.choice(np.flatnonzero(full_y_test == label), test_per_class, replace=False))
        train_indices = rng.permutation(train_indices)
        test_indices = rng.permutation(test_indices)
        return (
            full_x_train[train_indices].astype(np.float32) / 255.0,
            full_y_train[train_indices].astype(int),
            full_x_test[test_indices].astype(np.float32) / 255.0,
            full_y_test[test_indices].astype(int),
        )

    x_train, y_train, x_test, y_test = [], [], [], []
    for label in range(10):
        for sample_index in range(train_per_class):
            x_train.append(render_digit(label, rng, noisy=sample_index % 4 == 0))
            y_train.append(label)
        for _ in range(test_per_class):
            x_test.append(render_digit(label, rng, noisy=True))
            y_test.append(label)

    train_order = rng.permutation(len(x_train))
    test_order = rng.permutation(len(x_test))
    return (
        np.asarray(x_train)[train_order],
        np.asarray(y_train)[train_order],
        np.asarray(x_test)[test_order],
        np.asarray(y_test)[test_order],
    )


def corrupt_images(images: np.ndarray, seed: int = SEED + 7) -> np.ndarray:
    """Додає шум і невеликі стирання для перевірки стійкості CNN."""
    rng = np.random.default_rng(seed)
    corrupted = np.clip(images + rng.normal(0, 0.16, images.shape), 0, 1)
    for image in corrupted:
        if rng.random() < 0.35:
            row = int(rng.integers(6, 21))
            col = int(rng.integers(4, 12))
            image[row : row + 2, col : col + int(rng.integers(7, 14))] *= 0.15
    return corrupted.astype(np.float32)


class SimpleCNN:
    """Conv(8, 5x5) -> ReLU -> AvgPool(2x2) -> Dense(10)."""

    def __init__(self, seed: int = SEED):
        rng = np.random.default_rng(seed)
        self.filters = rng.normal(0, np.sqrt(2 / 25), size=(8, 5, 5)).astype(np.float32)
        self.conv_bias = np.zeros(8, dtype=np.float32)
        self.weights = rng.normal(0, np.sqrt(2 / (8 * 12 * 12)), size=(8 * 12 * 12, 10)).astype(np.float32)
        self.bias = np.zeros(10, dtype=np.float32)

    @staticmethod
    def _patches(x: np.ndarray) -> np.ndarray:
        return np.lib.stride_tricks.sliding_window_view(x, (5, 5), axis=(1, 2))

    def forward(self, x: np.ndarray):
        patches = self._patches(x)
        conv = np.einsum("bhwkl,fkl->bfhw", patches, self.filters) + self.conv_bias[None, :, None, None]
        relu = np.maximum(conv, 0)
        pooled = relu.reshape(len(x), 8, 12, 2, 12, 2).mean(axis=(3, 5))
        flat = pooled.reshape(len(x), -1)
        logits = flat @ self.weights + self.bias
        logits -= logits.max(axis=1, keepdims=True)
        probs = np.exp(logits)
        probs /= probs.sum(axis=1, keepdims=True)
        cache = (patches, conv, flat)
        return probs, cache

    def train_batch(self, x: np.ndarray, y: np.ndarray, lr: float) -> float:
        probs, (patches, conv, flat) = self.forward(x)
        n = len(x)
        loss = -np.log(probs[np.arange(n), y] + 1e-9).mean()

        dlogits = probs
        dlogits[np.arange(n), y] -= 1
        dlogits /= n
        dweights = flat.T @ dlogits
        dbias = dlogits.sum(axis=0)

        dflat = dlogits @ self.weights.T
        dpool = dflat.reshape(n, 8, 12, 12)
        drelu = np.repeat(np.repeat(dpool / 4.0, 2, axis=2), 2, axis=3)
        dconv = drelu * (conv > 0)
        dfilters = np.einsum("bfhw,bhwkl->fkl", dconv, patches)
        dconv_bias = dconv.sum(axis=(0, 2, 3))

        self.weights -= lr * dweights
        self.bias -= lr * dbias
        self.filters -= lr * dfilters
        self.conv_bias -= lr * dconv_bias
        return float(loss)

    def predict(self, x: np.ndarray, batch_size: int = 128) -> np.ndarray:
        predictions = []
        for start in range(0, len(x), batch_size):
            probs, _ = self.forward(x[start : start + batch_size])
            predictions.append(probs.argmax(axis=1))
        return np.concatenate(predictions)


def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    matrix = np.zeros((10, 10), dtype=int)
    for true, pred in zip(y_true, y_pred):
        matrix[true, pred] += 1
    return matrix


def main() -> None:
    x_train, y_train, x_test, y_test = generate_digit_dataset()
    model = SimpleCNN()
    rng = np.random.default_rng(SEED + 1)
    epochs, batch_size, learning_rate = 20, 50, 0.035
    history = []

    for epoch in range(epochs):
        order = rng.permutation(len(x_train))
        losses = []
        lr = learning_rate * (0.88 ** (epoch // 5))
        for start in range(0, len(order), batch_size):
            idx = order[start : start + batch_size]
            losses.append(model.train_batch(x_train[idx], y_train[idx], lr))
        train_pred = model.predict(x_train)
        test_pred = model.predict(x_test)
        history.append(
            (epoch + 1, float(np.mean(losses)), float(np.mean(train_pred == y_train)), float(np.mean(test_pred == y_test)))
        )

    test_pred = model.predict(x_test)
    x_test_corrupted = corrupt_images(x_test)
    corrupted_pred = model.predict(x_test_corrupted)
    matrix = confusion_matrix(y_test, test_pred)
    accuracy = float(np.mean(test_pred == y_test))
    corrupted_accuracy = float(np.mean(corrupted_pred == y_test))

    with (RESULTS / "training_history.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["epoch", "loss", "train_accuracy", "test_accuracy"])
        writer.writerows(history)
    np.savetxt(RESULTS / "confusion_matrix.csv", matrix, fmt="%d", delimiter=",")

    epochs_axis = [row[0] for row in history]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    axes[0].plot(epochs_axis, [row[1] for row in history], marker="o", color="#3366aa")
    axes[0].set(title="Функція втрат", xlabel="Епоха", ylabel="Cross-entropy")
    axes[0].grid(alpha=0.25)
    axes[1].plot(epochs_axis, [100 * row[2] for row in history], label="Навчальна")
    axes[1].plot(epochs_axis, [100 * row[3] for row in history], label="Тестова")
    axes[1].set(title="Точність", xlabel="Епоха", ylabel="Точність, %", ylim=(40, 101))
    axes[1].grid(alpha=0.25)
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(RESULTS / "training.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    image = ax.imshow(matrix, cmap="Blues")
    for i in range(10):
        for j in range(10):
            ax.text(j, i, matrix[i, j], ha="center", va="center", fontsize=7)
    ax.set(xlabel="Передбачений клас", ylabel="Правильний клас", title="Матриця помилок")
    ax.set_xticks(range(10)); ax.set_yticks(range(10))
    fig.colorbar(image, ax=ax, shrink=0.8)
    fig.tight_layout()
    fig.savefig(RESULTS / "confusion_matrix.png", dpi=180)
    plt.close(fig)

    clean_chosen = np.arange(min(20, len(x_train)))
    clean_pred = model.predict(x_train[clean_chosen])
    fig, axes = plt.subplots(2, 10, figsize=(12, 3.0))
    for ax, idx, pred in zip(axes.ravel(), clean_chosen, clean_pred):
        ax.imshow(x_train[idx], cmap="gray", vmin=0, vmax=1)
        color = "green" if pred == y_train[idx] else "crimson"
        ax.set_title(f"{y_train[idx]}→{pred}", color=color, fontsize=8)
        ax.axis("off")
    fig.suptitle("Розпізнавання чистих навчальних зображень")
    fig.tight_layout()
    fig.savefig(RESULTS / "clean_predictions.png", dpi=180)
    plt.close(fig)

    chosen = np.arange(min(30, len(x_test_corrupted)))
    fig, axes = plt.subplots(3, 10, figsize=(12, 4.2))
    for ax, idx in zip(axes.ravel(), chosen):
        ax.imshow(x_test_corrupted[idx], cmap="gray", vmin=0, vmax=1)
        color = "green" if corrupted_pred[idx] == y_test[idx] else "crimson"
        ax.set_title(f"{y_test[idx]}→{corrupted_pred[idx]}", color=color, fontsize=8)
        ax.axis("off")
    fig.suptitle("Розпізнавання зашумлених і частково пошкоджених цифр")
    fig.tight_layout()
    fig.savefig(RESULTS / "predictions.png", dpi=180)
    plt.close(fig)

    summary = (
        f"Train samples: {len(x_train)}\nTest samples: {len(x_test)}\n"
        f"Epochs: {epochs}\nTest accuracy: {accuracy:.6f}\nCorrupted accuracy: {corrupted_accuracy:.6f}\n"
        f"Final loss: {history[-1][1]:.6f}\n"
    )
    (RESULTS / "summary.txt").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
