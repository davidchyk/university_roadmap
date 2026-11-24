"""Лабораторна робота №8: оптимізація обчислювальної мережі ГА."""

from __future__ import annotations

from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
SEED = 4106
HOSTS, SWITCHES, CAPACITY = 24, 4, 6
SWITCH_POS = np.array([[10, 8], [30, 8], [50, 8], [70, 8]], dtype=float)
BACKBONE_CAPACITY = np.array([250.0, 250.0, 250.0])
MAX_CABLE_LENGTH = 55.0
LENGTH_PENALTY = 10.0


def make_problem():
    rng = np.random.default_rng(SEED)
    host_pos = np.column_stack([rng.uniform(2, 78, HOSTS), rng.uniform(14, 48, HOSTS)])
    communities = np.repeat(np.arange(4), 6)
    rng.shuffle(communities)
    traffic = rng.uniform(0.05, 0.4, size=(HOSTS, HOSTS))
    traffic = (traffic + traffic.T) / 2
    for i in range(HOSTS):
        for j in range(i + 1, HOSTS):
            if communities[i] == communities[j]:
                traffic[i, j] += rng.uniform(4.0, 9.0)
                traffic[j, i] = traffic[i, j]
            elif rng.random() < 0.08:
                traffic[i, j] += rng.uniform(1.0, 2.5)
                traffic[j, i] = traffic[i, j]
    np.fill_diagonal(traffic, 0)
    return host_pos, traffic, communities


def repair(chromosome: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    chromosome = chromosome.copy()
    counts = np.bincount(chromosome, minlength=SWITCHES)
    while np.any(counts > CAPACITY):
        source = int(np.argmax(counts))
        targets = np.flatnonzero(counts < CAPACITY)
        target = int(rng.choice(targets))
        candidates = np.flatnonzero(chromosome == source)
        chromosome[int(rng.choice(candidates))] = target
        counts[source] -= 1; counts[target] += 1
    return chromosome


def objective(chromosome: np.ndarray, host_pos: np.ndarray, traffic: np.ndarray):
    backbone = 0.0
    link_loads = np.zeros(SWITCHES - 1)
    for i in range(HOSTS):
        for j in range(i + 1, HOSTS):
            a, b = sorted((int(chromosome[i]), int(chromosome[j])))
            if a != b:
                backbone += traffic[i, j] * (b - a)
                link_loads[a:b] += traffic[i, j]
    cable_lengths = np.linalg.norm(host_pos - SWITCH_POS[chromosome], axis=1)
    cable = cable_lengths.sum()
    normalized_load = np.sum(link_loads / BACKBONE_CAPACITY)
    excess = np.maximum(cable_lengths - MAX_CABLE_LENGTH, 0.0)
    penalty = LENGTH_PENALTY * np.sum(excess**2)
    total = normalized_load + penalty
    return total, normalized_load, backbone, cable, link_loads, cable_lengths.max(), np.count_nonzero(excess)


def balanced_random(rng: np.random.Generator) -> np.ndarray:
    chromosome = np.repeat(np.arange(SWITCHES), CAPACITY)
    rng.shuffle(chromosome)
    return chromosome


def optimize(host_pos: np.ndarray, traffic: np.ndarray):
    rng = np.random.default_rng(SEED + 1)
    pop_size, generations = 80, 250
    population = np.asarray([balanced_random(rng) for _ in range(pop_size)])
    history_best, history_mean = [], []

    for _ in range(generations):
        scores = np.asarray([objective(ch, host_pos, traffic)[0] for ch in population])
        order = np.argsort(scores)
        history_best.append(float(scores[order[0]])); history_mean.append(float(scores.mean()))
        new_population = [population[i].copy() for i in order[:4]]
        scaled_fitness = scores.max() - scores
        if scaled_fitness.sum() <= 1e-12:
            selection_probabilities = np.full(pop_size, 1.0 / pop_size)
        else:
            selection_probabilities = scaled_fitness / scaled_fitness.sum()
        while len(new_population) < pop_size:
            parent_indices = rng.choice(pop_size, 2, replace=True, p=selection_probabilities)
            p1, p2 = population[parent_indices]
            if rng.random() < 0.90:
                point = int(rng.integers(1, HOSTS))
                child = np.concatenate([p1[:point], p2[point:]])
                child = repair(child, rng)
            else:
                child = p1.copy()
            if rng.random() < 0.15:
                a, b = rng.choice(HOSTS, 2, replace=False)
                child[a], child[b] = child[b], child[a]
            new_population.append(child)
        population = np.asarray(new_population)

    scores = np.asarray([objective(ch, host_pos, traffic)[0] for ch in population])
    return population[np.argmin(scores)], np.asarray(history_best), np.asarray(history_mean)


def plot_topology(path: Path, assignment: np.ndarray, host_pos: np.ndarray, title: str):
    colors = ["#3366aa", "#dd5533", "#33aa66", "#8844aa"]
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.plot(SWITCH_POS[:, 0], SWITCH_POS[:, 1], "k-", linewidth=3, label="Магістраль")
    for host in range(HOSTS):
        switch = assignment[host]
        ax.plot([host_pos[host, 0], SWITCH_POS[switch, 0]], [host_pos[host, 1], SWITCH_POS[switch, 1]], color=colors[switch], alpha=0.32)
        ax.scatter(*host_pos[host], color=colors[switch], s=30)
        ax.text(host_pos[host, 0] + 0.6, host_pos[host, 1] + 0.3, str(host + 1), fontsize=7)
    ax.scatter(SWITCH_POS[:, 0], SWITCH_POS[:, 1], marker="s", s=150, color="black")
    for i, pos in enumerate(SWITCH_POS): ax.text(pos[0], pos[1] - 3.2, f"S{i + 1}", ha="center")
    ax.set(xlabel="X", ylabel="Y", title=title, xlim=(0, 82), ylim=(3, 52))
    ax.grid(alpha=0.15); fig.tight_layout(); fig.savefig(path, dpi=180); plt.close(fig)


def main() -> None:
    host_pos, traffic, communities = make_problem()
    baseline = np.argmin(np.linalg.norm(host_pos[:, None, :] - SWITCH_POS[None, :, :], axis=2), axis=1)
    baseline = repair(baseline, np.random.default_rng(SEED + 2))
    optimized, history_best, history_mean = optimize(host_pos, traffic)
    before = objective(baseline, host_pos, traffic)
    after = objective(optimized, host_pos, traffic)
    improvement = 100 * (before[0] - after[0]) / before[0]

    plot_topology(RESULTS / "topology_before.png", baseline, host_pos, "Початкове підключення за відстанню")
    plot_topology(RESULTS / "topology_after.png", optimized, host_pos, "Підключення після генетичної оптимізації")

    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.plot(history_best, label="Найкраще значення"); ax.plot(history_mean, label="Середнє значення", alpha=0.75)
    ax.set_yscale("log")
    ax.set(xlabel="Покоління", ylabel="Цільова функція (логарифмічна шкала)", title="Збіжність генетичного алгоритму")
    ax.grid(alpha=0.25); ax.legend(); fig.tight_layout(); fig.savefig(RESULTS / "convergence.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    positions = np.arange(1, SWITCHES)
    width = 0.36
    ax.bar(positions - width / 2, before[4], width, label="До оптимізації")
    ax.bar(positions + width / 2, after[4], width, label="Після оптимізації")
    ax.axhline(BACKBONE_CAPACITY[0], color="crimson", linestyle="--", label="Пропускна здатність")
    ax.set_xticks(positions, ["S1-S2", "S2-S3", "S3-S4"])
    ax.set(ylabel="Трафік магістрального каналу", title="Навантаження каналів магістралі")
    ax.grid(axis="y", alpha=0.25); ax.legend(); fig.tight_layout(); fig.savefig(RESULTS / "backbone_loads.png", dpi=180); plt.close(fig)

    with (RESULTS / "assignments.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["host", "community", "baseline_switch", "optimized_switch"])
        for i in range(HOSTS): writer.writerow([i + 1, communities[i] + 1, baseline[i] + 1, optimized[i] + 1])

    summary = (
        f"Hosts: {HOSTS}\nSwitches: {SWITCHES}\nCapacity: {CAPACITY}\nPopulation: 80\nGenerations: 250\n"
        f"Baseline objective: {before[0]:.6f}\nOptimized objective: {after[0]:.6f}\n"
        f"Baseline normalized load: {before[1]:.6f}\nOptimized normalized load: {after[1]:.6f}\n"
        f"Baseline backbone: {before[2]:.6f}\nOptimized backbone: {after[2]:.6f}\n"
        f"Baseline cable: {before[3]:.6f}\nOptimized cable: {after[3]:.6f}\n"
        f"Baseline max cable: {before[5]:.6f}\nOptimized max cable: {after[5]:.6f}\n"
        f"Baseline length violations: {before[6]}\nOptimized length violations: {after[6]}\n"
        f"Improvement percent: {improvement:.6f}\n"
    )
    (RESULTS / "summary.txt").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
