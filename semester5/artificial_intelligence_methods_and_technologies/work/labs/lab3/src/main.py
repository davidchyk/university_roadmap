"""Лабораторна робота №3: дослідження Fuzzy C-Means.

Задача: нечітко класифікувати мережеві пристрої за двома ознаками:
середня затримка відповіді та кількість пакетів за хвилину.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "results"


def make_dataset(seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    centers = np.array([[20.0, 20.0], [75.0, 55.0], [45.0, 110.0]])
    scales = np.array([[7.0, 8.0], [9.0, 10.0], [8.0, 13.0]])
    groups = [center + rng.normal(size=(120, 2)) * scale for center, scale in zip(centers, scales)]
    return np.vstack(groups)


def fuzzy_c_means(data: np.ndarray, clusters: int = 3, fuzziness: float = 2.0,
                  error: float = 0.005, max_iter: int = 100, seed: int = 42):
    rng = np.random.default_rng(seed)
    objects = len(data)
    membership = rng.random((clusters, objects))
    membership /= membership.sum(axis=0, keepdims=True)
    objective_history = []

    for iteration in range(max_iter):
        weights = membership ** fuzziness
        centers = (weights @ data) / weights.sum(axis=1, keepdims=True)
        distances = np.linalg.norm(data[None, :, :] - centers[:, None, :], axis=2)
        distances = np.maximum(distances, 1e-12)
        objective = float(np.sum(weights * distances**2))
        objective_history.append(objective)

        ratios = (distances[:, None, :] / distances[None, :, :]) ** (2.0 / (fuzziness - 1.0))
        updated = 1.0 / ratios.sum(axis=1)
        if np.linalg.norm(updated - membership) < error:
            membership = updated
            break
        membership = updated

    labels = np.argmax(membership, axis=0)
    return centers, membership, labels, np.asarray(objective_history), iteration + 1


def save_cluster_plot(data, centers, labels, path):
    plt.figure(figsize=(9, 6))
    for cluster in range(len(centers)):
        points = data[labels == cluster]
        plt.scatter(points[:, 0], points[:, 1], s=18, alpha=0.7, label=f"Кластер {cluster + 1}")
    plt.scatter(centers[:, 0], centers[:, 1], marker="*", s=240, color="black", label="Центри")
    plt.xlabel("Середня затримка, мс")
    plt.ylabel("Пакети за хвилину")
    plt.title("Нечітка кластеризація мережевих пристроїв")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = make_dataset()
    centers, membership, labels, objective, iterations = fuzzy_c_means(data)

    save_cluster_plot(data, centers, labels, OUTPUT_DIR / "clusters.png")
    plt.figure(figsize=(8, 5))
    plt.plot(np.arange(1, len(objective) + 1), objective, marker="o", ms=3)
    plt.xlabel("Номер ітерації")
    plt.ylabel("Значення цільової функції")
    plt.title("Зміна цільової функції FCM")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "objective.png", dpi=180)
    plt.close()

    np.savetxt(OUTPUT_DIR / "cluster_centers.csv", centers, delimiter=",", header="latency,packets", comments="")
    np.savetxt(OUTPUT_DIR / "membership_matrix.csv", membership, delimiter=",")
    np.savetxt(OUTPUT_DIR / "objective.csv", objective, delimiter=",", header="objective", comments="")
    with (OUTPUT_DIR / "summary.txt").open("w", encoding="utf-8") as file:
        file.write(f"Кількість об'єктів: {len(data)}\n")
        file.write(f"Кількість кластерів: {len(centers)}\n")
        file.write(f"Показник нечіткості q: 2.0\n")
        file.write(f"Кількість ітерацій: {iterations}\n")
        file.write("Центри кластерів (затримка, пакети/хв):\n")
        for number, center in enumerate(centers, start=1):
            file.write(f"  {number}: {center[0]:.4f}, {center[1]:.4f}\n")

    print(f"Результати збережено у {OUTPUT_DIR}")
    print(f"Ітерацій: {iterations}")
    for number, center in enumerate(centers, start=1):
        print(f"Кластер {number}: latency={center[0]:.3f}, packets={center[1]:.3f}")


if __name__ == "__main__":
    main()
