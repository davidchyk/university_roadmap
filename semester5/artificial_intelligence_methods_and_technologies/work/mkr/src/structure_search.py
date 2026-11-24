"""Genetic structural synthesis of a feed-forward neural network."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from mkr_core import FeedForwardNetwork, GAConfig, train_genetic


@dataclass
class StructureConfig:
    max_total_neurons: int = 30
    max_hidden_layers: int = 5
    population_size: int = 8
    generations: int = 6
    inner_population: int = 20
    inner_generations: int = 35
    target_mse: float = 0.01
    complexity_penalty: float = 0.00002
    seed: int = 4106


def _repair(genome: np.ndarray, config: StructureConfig) -> np.ndarray:
    genome = np.clip(np.rint(genome), 0, config.max_total_neurons).astype(int)
    if not np.any(genome):
        genome[0] = 2
    nonzero = genome[genome > 0]
    total = int(nonzero.sum())
    while total > config.max_total_neurons:
        index = int(np.argmax(genome))
        if genome[index] > 1:
            genome[index] -= 1
        else:
            genome[index] = 0
        total = int(genome[genome > 0].sum())
    compact = np.zeros_like(genome)
    compact[: len(nonzero := genome[genome > 0])] = nonzero
    return compact


def _architecture(genome: np.ndarray) -> tuple[int, ...]:
    return (2, *[int(value) for value in genome if value > 0], 1)


def search_architecture(
    train_inputs: np.ndarray,
    train_targets: np.ndarray,
    validation_inputs: np.ndarray,
    validation_targets: np.ndarray,
    config: StructureConfig,
    callback: Callable[[int, tuple[int, ...], float], None] | None = None,
) -> dict:
    """Outer GA evolves architecture; inner GA trains candidate weights."""
    rng = np.random.default_rng(config.seed)
    population = []
    for _ in range(config.population_size):
        layers = int(rng.integers(1, config.max_hidden_layers + 1))
        genome = np.zeros(config.max_hidden_layers, dtype=int)
        genome[:layers] = rng.integers(2, max(3, config.max_total_neurons // layers + 1), size=layers)
        population.append(_repair(genome, config))
    population = np.asarray(population)
    cache: dict[tuple[int, ...], tuple[float, float, np.ndarray]] = {}
    history = []
    all_candidates = []

    def evaluate(genome: np.ndarray, generation: int):
        architecture = _architecture(genome)
        if architecture not in cache:
            network = FeedForwardNetwork(architecture)
            candidate_seed = config.seed + sum((index + 1) * value for index, value in enumerate(architecture))
            trained = train_genetic(
                network,
                train_inputs,
                train_targets,
                GAConfig(
                    population_size=config.inner_population,
                    generations=config.inner_generations,
                    elite_count=2,
                    tournament_size=3,
                    mutation_probability=0.05,
                    seed=candidate_seed,
                    patience=config.inner_generations,
                ),
                initialization="nguyen_widrow",
            )
            prediction = network.forward(validation_inputs, trained["chromosome"])
            mse = float(np.mean((prediction - validation_targets) ** 2))
            fitness = mse + config.complexity_penalty * sum(architecture[1:-1])
            cache[architecture] = (fitness, mse, trained["chromosome"])
            all_candidates.append({"generation": generation, "architecture": architecture, "mse": mse})
        return cache[architecture]

    best_architecture = None
    best_mse = float("inf")
    best_chromosome = None
    for generation in range(config.generations):
        evaluated = [evaluate(genome, generation + 1) for genome in population]
        scores = np.asarray([item[0] for item in evaluated])
        order = np.argsort(scores)
        architecture = _architecture(population[order[0]])
        current_mse = evaluated[order[0]][1]
        history.append(current_mse)
        if current_mse < best_mse:
            best_architecture = architecture
            best_mse = current_mse
            best_chromosome = evaluated[order[0]][2]
        if callback is not None:
            callback(generation + 1, architecture, current_mse)
        if best_mse <= config.target_mse:
            break

        new_population = [population[index].copy() for index in order[:2]]

        def tournament():
            indices = rng.choice(len(population), min(3, len(population)), replace=False)
            return population[indices[np.argmin(scores[indices])]]

        while len(new_population) < config.population_size:
            parent_a, parent_b = tournament(), tournament()
            point = int(rng.integers(1, config.max_hidden_layers))
            child = np.concatenate([parent_a[:point], parent_b[point:]])
            if rng.random() < 0.35:
                gene = int(rng.integers(config.max_hidden_layers))
                child[gene] += int(rng.choice([-2, -1, 1, 2]))
            new_population.append(_repair(child, config))
        population = np.asarray(new_population)

    return {
        "architecture": best_architecture,
        "mse": best_mse,
        "chromosome": best_chromosome,
        "history": np.asarray(history),
        "candidates": all_candidates,
    }
