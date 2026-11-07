"""Лабораторна робота №4: моделювання функції нейронними мережами.

Варіант 6: y = sin(|x|) + cos(|x|), z = x * sin(y).
Порівнюються шість конфігурацій feed-forward, cascade-forward та Elman.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "results"


def function_z(x, y):
    return x * np.sin(y)


def make_dataset(seed=42):
    rng = np.random.default_rng(seed)
    x = np.linspace(0.0, 1.0, 25)
    y = np.linspace(1.0, np.sin(1.0) + np.cos(1.0), 25)
    xx, yy = np.meshgrid(x, y)
    features = np.column_stack((xx.ravel(), yy.ravel()))
    target = function_z(features[:, 0], features[:, 1])[:, None]
    order = rng.permutation(len(features))
    split = int(len(features) * 0.8)
    train = order[:split]
    test = order[split:]
    return features[train], target[train], features[test], target[test], features, target


class DenseModel:
    def __init__(self, input_size, hidden_layers, kind, seed=42):
        self.kind = kind
        self.hidden_layers = hidden_layers
        rng = np.random.default_rng(seed)
        self.weights = []
        self.biases = []
        previous = input_size
        for index, neurons in enumerate(hidden_layers):
            if kind == "feedforward":
                current_input = previous
            elif index == 0:
                current_input = input_size
            else:
                current_input = input_size + previous
            self.weights.append(rng.normal(0, np.sqrt(2 / current_input), (current_input, neurons)))
            self.biases.append(np.zeros((1, neurons)))
            previous = neurons
        output_input = previous if kind == "feedforward" else input_size + previous
        self.weights.append(rng.normal(0, np.sqrt(2 / output_input), (output_input, 1)))
        self.biases.append(np.zeros((1, 1)))

    def forward(self, inputs, training=False):
        states = [inputs]
        preactivations = []
        current = inputs
        for index, (weight, bias) in enumerate(zip(self.weights[:-1], self.biases[:-1])):
            if self.kind == "feedforward":
                layer_input = current
            else:
                layer_input = np.concatenate((inputs, current), axis=1) if index else inputs
            pre = layer_input @ weight + bias
            current = np.tanh(pre)
            preactivations.append((layer_input, pre))
            states.append(current)
        if self.kind == "feedforward":
            output_input = current
        else:
            output_input = np.concatenate((inputs, current), axis=1)
        output = output_input @ self.weights[-1] + self.biases[-1]
        return output, states, preactivations, output_input

    def fit(self, inputs, target, epochs=350, learning_rate=0.035):
        history = []
        for _ in range(epochs):
            output, states, preacts, output_input = self.forward(inputs, training=True)
            error = output - target
            history.append(float(np.mean(error**2)))
            grad_w = [None] * len(self.weights)
            grad_b = [None] * len(self.biases)
            grad_output = 2 * error / len(inputs)
            grad_w[-1] = output_input.T @ grad_output
            grad_b[-1] = grad_output.sum(axis=0, keepdims=True)
            grad_current = grad_output @ self.weights[-1].T
            if self.kind != "feedforward":
                grad_current = grad_current[:, -states[-1].shape[1]:]
            for index in reversed(range(len(self.hidden_layers))):
                layer_input, pre = preacts[index]
                grad_pre = grad_current * (1 - np.tanh(pre) ** 2)
                grad_w[index] = layer_input.T @ grad_pre
                grad_b[index] = grad_pre.sum(axis=0, keepdims=True)
                propagated = grad_pre @ self.weights[index].T
                if self.kind == "feedforward":
                    grad_current = propagated
                else:
                    grad_current = propagated[:, -states[index].shape[1]:] if index else None
            for index in range(len(self.weights)):
                self.weights[index] -= learning_rate * np.clip(grad_w[index], -5, 5)
                self.biases[index] -= learning_rate * np.clip(grad_b[index], -5, 5)
        return np.asarray(history)


class ElmanModel(DenseModel):
    """Elman-подібна модель: попередній прихований стан подається як контекст.

    Для регресії статичної функції контекст розраховується послідовно на сітці,
    а ваги навчаються за усередненим градієнтом поточного кроку.
    """

    def __init__(self, input_size, hidden_layers, seed=42):
        super().__init__(input_size, hidden_layers, "feedforward", seed)
        self.context_weights = []
        rng = np.random.default_rng(seed + 100)
        previous = input_size
        for neurons in hidden_layers:
            self.context_weights.append(rng.normal(0, 0.05, (neurons, neurons)))
            previous = neurons

    def forward(self, inputs, training=False):
        states = [inputs]
        preactivations = []
        for index, (weight, bias) in enumerate(zip(self.weights[:-1], self.biases[:-1])):
            previous_context = np.zeros((1, self.hidden_layers[index]))
            layer_inputs = inputs if index == 0 else states[-1]
            layer_values = []
            layer_pre = []
            for row in range(len(inputs)):
                layer_input = layer_inputs[row:row + 1]
                pre = layer_input @ weight + previous_context @ self.context_weights[index] + bias
                current = np.tanh(pre)
                layer_values.append(current[0])
                layer_pre.append(pre[0])
                previous_context = current
            current = np.asarray(layer_values)
            preactivations.append((layer_inputs, np.asarray(layer_pre)))
            states.append(current)
        output = states[-1] @ self.weights[-1] + self.biases[-1]
        return output, states, preactivations, states[-1]


def relative_error(actual, predicted):
    return np.mean(np.abs(actual - predicted) / np.abs(actual + 1.0)) * 100


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    x_train, z_train, x_test, z_test, all_x, all_z = make_dataset()
    configurations = [
        ("feedforward_1x10", "feedforward", [10]),
        ("feedforward_1x20", "feedforward", [20]),
        ("cascade_1x20", "cascade", [20]),
        ("cascade_2x10", "cascade", [10, 10]),
        ("elman_1x15", "elman", [15]),
        ("elman_3x5", "elman", [5, 5, 5]),
    ]
    rows = []
    histories = {}
    predictions = {}
    for number, (name, kind, layers) in enumerate(configurations):
        model = ElmanModel(2, layers, seed=number + 10) if kind == "elman" else DenseModel(2, layers, kind, seed=number + 10)
        history = model.fit(x_train, z_train)
        prediction = model.forward(x_test)[0]
        full_prediction = model.forward(all_x)[0]
        rows.append((name, len(layers), sum(layers), relative_error(z_test, prediction), history[-1]))
        histories[name] = history
        predictions[name] = full_prediction[:, 0]

    with (OUTPUT_DIR / "results.csv").open("w", encoding="utf-8") as file:
        file.write("Мережа,Кількість шарів,Нейронів,Середня відносна похибка %,Фінальна MSE\n")
        for row in rows:
            file.write(f"{row[0]},{row[1]},{row[2]},{row[3]:.6f},{row[4]:.8f}\n")

    plt.figure(figsize=(10, 6))
    for name, history in histories.items():
        plt.plot(history, label=name)
    plt.yscale("log")
    plt.xlabel("Епоха")
    plt.ylabel("MSE, логарифмічна шкала")
    plt.title("Залежність помилки від епохи навчання")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "training_loss.png", dpi=180)
    plt.close()

    best = min(rows, key=lambda row: row[3])
    for name, prediction in predictions.items():
        figure = plt.figure(figsize=(9, 6))
        axes = figure.add_subplot(111, projection="3d")
        axes.scatter(all_x[:, 0], all_x[:, 1], all_z[:, 0], s=8, label="Точна функція")
        axes.scatter(all_x[:, 0], all_x[:, 1], prediction, s=8, label="Нейромережа")
        axes.set_xlabel("x")
        axes.set_ylabel("y")
        axes.set_zlabel("z")
        axes.set_title(name)
        axes.legend()
        figure.tight_layout()
        figure.savefig(OUTPUT_DIR / f"surface_{name}.png", dpi=160)
        plt.close(figure)

    with (OUTPUT_DIR / "summary.txt").open("w", encoding="utf-8") as file:
        file.write(f"Найменша тестова похибка: {best[0]} = {best[3]:.6f}%\n")
        for row in rows:
            file.write(f"{row[0]}: {row[3]:.6f}%\n")

    print(f"Результати збережено у {OUTPUT_DIR}")
    for row in rows:
        print(f"{row[0]:18} error={row[3]:.5f}%")


if __name__ == "__main__":
    main()
