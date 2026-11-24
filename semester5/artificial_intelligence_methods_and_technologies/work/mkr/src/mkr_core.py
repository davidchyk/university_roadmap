"""Core algorithms for the modular control work.

The module intentionally implements forward propagation, the genetic
algorithm and Adam/backpropagation directly with NumPy.
"""

from __future__ import annotations

from dataclasses import dataclass
import ast
import math
from typing import Callable, Iterable

import numpy as np


Array = np.ndarray


def target_function(x: Array, y: Array) -> Array:
    """Variant 52: z = x * sin(|y|)."""
    return x * np.sin(np.abs(y))


def make_grid(
    x_interval: tuple[float, float] = (0.0, 1.0),
    y_interval: tuple[float, float] = (0.0, 1.0),
    points: int = 31,
    function: Callable[[Array, Array], Array] = target_function,
) -> tuple[Array, Array, Array, Array]:
    x_axis = np.linspace(*x_interval, points)
    y_axis = np.linspace(*y_interval, points)
    xx, yy = np.meshgrid(x_axis, y_axis)
    inputs = np.column_stack([xx.ravel(), yy.ravel()])
    targets = function(inputs[:, 0], inputs[:, 1]).reshape(-1, 1)
    return inputs, targets, xx, yy


def split_dataset(inputs: Array, targets: Array, test_fraction: float = 0.2, seed: int = 4106):
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(inputs))
    test_count = int(round(len(inputs) * test_fraction))
    test_indices = order[:test_count]
    train_indices = order[test_count:]
    return inputs[train_indices], targets[train_indices], inputs[test_indices], targets[test_indices]


class FeedForwardNetwork:
    """Dense tanh network with a linear output layer."""

    def __init__(self, architecture: Iterable[int]):
        self.architecture = tuple(int(value) for value in architecture)
        if len(self.architecture) < 2 or self.architecture[0] != 2 or self.architecture[-1] != 1:
            raise ValueError("Architecture must start with 2 inputs and end with 1 output")
        self.shapes = [
            (self.architecture[index], self.architecture[index + 1])
            for index in range(len(self.architecture) - 1)
        ]
        self.parameter_count = sum(rows * columns + columns for rows, columns in self.shapes)

    def unpack(self, chromosome: Array) -> tuple[list[Array], list[Array]]:
        chromosome = np.asarray(chromosome, dtype=float)
        if chromosome.size != self.parameter_count:
            raise ValueError(f"Expected {self.parameter_count} parameters, got {chromosome.size}")
        weights, biases = [], []
        cursor = 0
        for rows, columns in self.shapes:
            weight_count = rows * columns
            weights.append(chromosome[cursor : cursor + weight_count].reshape(rows, columns))
            cursor += weight_count
            biases.append(chromosome[cursor : cursor + columns].reshape(1, columns))
            cursor += columns
        return weights, biases

    @staticmethod
    def pack(weights: list[Array], biases: list[Array]) -> Array:
        parts = []
        for weight, bias in zip(weights, biases):
            parts.extend((weight.ravel(), bias.ravel()))
        return np.concatenate(parts)

    def forward(self, inputs: Array, chromosome: Array, return_cache: bool = False):
        weights, biases = self.unpack(chromosome)
        activation = np.asarray(inputs, dtype=float)
        activations = [activation]
        for index, (weight, bias) in enumerate(zip(weights, biases)):
            linear = activation @ weight + bias
            activation = linear if index == len(weights) - 1 else np.tanh(linear)
            activations.append(activation)
        if return_cache:
            return activation, activations, weights, biases
        return activation


def error_metrics(expected: Array, predicted: Array) -> dict[str, float]:
    difference = np.asarray(predicted) - np.asarray(expected)
    return {
        "mse": float(np.mean(difference**2)),
        "rmse": float(np.sqrt(np.mean(difference**2))),
        "mae": float(np.mean(np.abs(difference))),
        "max_abs": float(np.max(np.abs(difference))),
    }


def xavier_chromosome(network: FeedForwardNetwork, rng: np.random.Generator) -> Array:
    weights, biases = [], []
    for fan_in, fan_out in network.shapes:
        limit = math.sqrt(6.0 / (fan_in + fan_out))
        weights.append(rng.uniform(-limit, limit, size=(fan_in, fan_out)))
        biases.append(np.zeros((1, fan_out)))
    return network.pack(weights, biases)


def estimate_feature_significance(inputs: Array, targets: Array) -> Array:
    """Estimate prior input importance using absolute standardized correlation."""
    target = targets.ravel()
    scores = []
    for column in inputs.T:
        if np.std(column) < 1e-12 or np.std(target) < 1e-12:
            scores.append(1.0)
        else:
            scores.append(abs(float(np.corrcoef(column, target)[0, 1])))
    scores = np.asarray(scores) + 1e-3
    return scores / scores.sum()


def nguyen_widrow_chromosome(
    network: FeedForwardNetwork,
    rng: np.random.Generator,
    feature_significance: Array,
) -> Array:
    """Modified Nguyen-Widrow initialization with feature-aware first layer."""
    weights, biases = [], []
    for layer_index, (fan_in, fan_out) in enumerate(network.shapes):
        raw = rng.uniform(-0.5, 0.5, size=(fan_in, fan_out))
        if layer_index == 0:
            raw = raw * np.sqrt(feature_significance[:, None] * len(feature_significance))
        norms = np.linalg.norm(raw, axis=0, keepdims=True)
        beta = 0.7 * fan_out ** (1.0 / max(fan_in, 1))
        weight = beta * raw / np.maximum(norms, 1e-12)
        bias = rng.uniform(-beta, beta, size=(1, fan_out))
        weights.append(weight)
        biases.append(bias)
    return network.pack(weights, biases)


@dataclass
class GAConfig:
    population_size: int = 80
    generations: int = 250
    elite_count: int = 4
    tournament_size: int = 4
    crossover_probability: float = 0.90
    mutation_probability: float = 0.035
    mutation_sigma_start: float = 0.12
    mutation_sigma_end: float = 0.008
    seed: int = 4106
    patience: int = 70


def train_genetic(
    network: FeedForwardNetwork,
    inputs: Array,
    targets: Array,
    config: GAConfig,
    initialization: str = "random",
    callback: Callable[[int, float, float], None] | None = None,
) -> dict:
    """Train all network parameters with a real-valued genetic algorithm."""
    rng = np.random.default_rng(config.seed)
    importance = estimate_feature_significance(inputs, targets)
    population = []
    if initialization == "nguyen_widrow":
        for _ in range(config.population_size):
            chromosome = nguyen_widrow_chromosome(network, rng, importance)
            chromosome += rng.normal(0.0, 0.03, size=network.parameter_count)
            population.append(chromosome)
    elif initialization == "random":
        population = [xavier_chromosome(network, rng) for _ in range(config.population_size)]
    else:
        raise ValueError("initialization must be 'random' or 'nguyen_widrow'")
    population = np.asarray(population)

    def evaluate(chromosomes: Array) -> Array:
        return np.asarray([
            np.mean((network.forward(inputs, chromosome) - targets) ** 2)
            for chromosome in chromosomes
        ])

    best_history, mean_history = [], []
    best_chromosome = population[0].copy()
    best_score = float("inf")
    stale = 0

    for generation in range(config.generations):
        scores = evaluate(population)
        order = np.argsort(scores)
        generation_best = float(scores[order[0]])
        best_history.append(generation_best)
        mean_history.append(float(scores.mean()))
        if generation_best < best_score - 1e-12:
            best_score = generation_best
            best_chromosome = population[order[0]].copy()
            stale = 0
        else:
            stale += 1
        if callback is not None:
            callback(generation + 1, generation_best, float(scores.mean()))
        if stale >= config.patience:
            break

        progress = generation / max(config.generations - 1, 1)
        sigma = config.mutation_sigma_start * (1.0 - progress) + config.mutation_sigma_end * progress
        new_population = [population[index].copy() for index in order[: config.elite_count]]

        def tournament() -> Array:
            candidates = rng.choice(len(population), config.tournament_size, replace=False)
            return population[candidates[np.argmin(scores[candidates])]]

        while len(new_population) < config.population_size:
            parent_a, parent_b = tournament(), tournament()
            if rng.random() < config.crossover_probability:
                alpha = rng.uniform(-0.15, 1.15, size=network.parameter_count)
                child = alpha * parent_a + (1.0 - alpha) * parent_b
            else:
                child = parent_a.copy()
            mutation_mask = rng.random(network.parameter_count) < config.mutation_probability
            child += mutation_mask * rng.normal(0.0, sigma, size=network.parameter_count)
            new_population.append(np.clip(child, -4.0, 4.0))
        population = np.asarray(new_population)

    return {
        "chromosome": best_chromosome,
        "best_history": np.asarray(best_history),
        "mean_history": np.asarray(mean_history),
        "best_mse": best_score,
        "generations_completed": len(best_history),
        "feature_significance": importance,
    }


@dataclass
class AdamConfig:
    epochs: int = 1200
    learning_rate: float = 0.003
    batch_size: int = 64
    seed: int = 4106
    beta1: float = 0.9
    beta2: float = 0.999
    epsilon: float = 1e-8


def train_adam(
    network: FeedForwardNetwork,
    inputs: Array,
    targets: Array,
    config: AdamConfig,
) -> dict:
    """Self-contained backpropagation and Adam optimizer implementation."""
    rng = np.random.default_rng(config.seed)
    chromosome = xavier_chromosome(network, rng)
    first_moment = np.zeros_like(chromosome)
    second_moment = np.zeros_like(chromosome)
    history = []
    step = 0

    for _ in range(config.epochs):
        order = rng.permutation(len(inputs))
        for start in range(0, len(inputs), config.batch_size):
            indices = order[start : start + config.batch_size]
            batch_inputs, batch_targets = inputs[indices], targets[indices]
            prediction, activations, weights, biases = network.forward(
                batch_inputs, chromosome, return_cache=True
            )
            delta = 2.0 * (prediction - batch_targets) / len(batch_inputs)
            weight_gradients = [np.zeros_like(weight) for weight in weights]
            bias_gradients = [np.zeros_like(bias) for bias in biases]

            for layer in reversed(range(len(weights))):
                weight_gradients[layer] = activations[layer].T @ delta
                bias_gradients[layer] = delta.sum(axis=0, keepdims=True)
                if layer > 0:
                    delta = (delta @ weights[layer].T) * (1.0 - activations[layer] ** 2)

            gradient = network.pack(weight_gradients, bias_gradients)
            step += 1
            first_moment = config.beta1 * first_moment + (1.0 - config.beta1) * gradient
            second_moment = config.beta2 * second_moment + (1.0 - config.beta2) * gradient**2
            corrected_first = first_moment / (1.0 - config.beta1**step)
            corrected_second = second_moment / (1.0 - config.beta2**step)
            chromosome -= config.learning_rate * corrected_first / (
                np.sqrt(corrected_second) + config.epsilon
            )
        history.append(float(np.mean((network.forward(inputs, chromosome) - targets) ** 2)))

    return {"chromosome": chromosome, "history": np.asarray(history), "epochs_completed": config.epochs}


_ALLOWED_FUNCTIONS = {
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "abs": np.abs,
    "sqrt": np.sqrt,
    "exp": np.exp,
    "log": np.log,
}


def compile_safe_expression(expression: str) -> Callable[[Array, Array], Array]:
    """Compile a small mathematical expression without using eval on arbitrary code."""
    tree = ast.parse(expression, mode="eval")
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Call,
        ast.Name,
        ast.Load,
        ast.Constant,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.USub,
        ast.UAdd,
    )
    for node in ast.walk(tree):
        if not isinstance(node, allowed_nodes):
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")
        if isinstance(node, ast.Name) and node.id not in {"x", "y", *list(_ALLOWED_FUNCTIONS)}:
            raise ValueError(f"Unknown name: {node.id}")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_FUNCTIONS:
                raise ValueError("Only approved mathematical functions are allowed")
    code = compile(tree, "<function>", "eval")

    def function(x: Array, y: Array) -> Array:
        namespace = {"x": x, "y": y, **_ALLOWED_FUNCTIONS}
        return np.asarray(eval(code, {"__builtins__": {}}, namespace), dtype=float)

    return function
