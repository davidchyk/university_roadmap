from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
RESULTS = PROJECT / "results"
SOURCE = PROJECT.parent / "lab4" / "src"
RNG = np.random.default_rng(4106)

SEGMENT_CLUSTERS = 6
SCENE_CLUSTERS = 4
PATCHES_PER_IMAGE = 6
MAX_SEGMENT_SIDE = 420


def load_rgb(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.uint8)


def resize_for_segmentation(image: np.ndarray) -> np.ndarray:
    h, w = image.shape[:2]
    scale = min(1.0, MAX_SEGMENT_SIDE / max(h, w))
    size = (max(1, round(w * scale)), max(1, round(h * scale)))
    return np.asarray(Image.fromarray(image).resize(size, Image.Resampling.LANCZOS))


def kmeans(data: np.ndarray, k: int, iterations: int = 60) -> tuple[np.ndarray, np.ndarray]:
    """K-means без бібліотек ML; повертає центри та номер кластера."""
    data = np.asarray(data, dtype=np.float64)
    centers = data[RNG.choice(len(data), size=k, replace=False)].copy()
    labels = np.zeros(len(data), dtype=np.int32)
    for _ in range(iterations):
        distances = ((data[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        new_labels = distances.argmin(axis=1)
        new_centers = centers.copy()
        for index in range(k):
            members = data[new_labels == index]
            if len(members):
                new_centers[index] = members.mean(axis=0)
        if np.array_equal(labels, new_labels) and np.allclose(centers, new_centers):
            break
        labels, centers = new_labels, new_centers
    return centers, labels


def segment(image: np.ndarray, k: int = SEGMENT_CLUSTERS) -> tuple[np.ndarray, np.ndarray]:
    small = resize_for_segmentation(image)
    pixels = small.reshape(-1, 3) / 255.0
    # RGB доповнено координатами: сегменти стають просторово зв'язнішими.
    h, w = small.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    features = np.column_stack(
        [pixels, 0.22 * xx.ravel() / w, 0.22 * yy.ravel() / h]
    )
    centers, labels = kmeans(features, k)
    palette = np.clip(centers[:, :3] * 255, 0, 255).astype(np.uint8)
    segmented = palette[labels].reshape(h, w, 3)
    return small, segmented


def patch_features(image: np.ndarray) -> np.ndarray:
    """Ознаки фрагмента: статистики кольору, яскравості та текстури."""
    rgb = image.astype(np.float64) / 255.0
    gray = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    gx = np.abs(np.diff(gray, axis=1)).mean()
    gy = np.abs(np.diff(gray, axis=0)).mean()
    hist = np.histogram(gray, bins=8, range=(0, 1), density=True)[0]
    return np.concatenate([rgb.mean((0, 1)), rgb.std((0, 1)), [gx, gy], hist])


def build_dataset(images: list[tuple[str, np.ndarray]]) -> tuple[list[np.ndarray], list[str]]:
    patches: list[np.ndarray] = []
    names: list[str] = []
    for source_name, image in images:
        h, w = image.shape[:2]
        ph, pw = h // 3, w // 4
        coords = [(r * ph, c * pw) for r in range(3) for c in range(4)]
        selected = RNG.choice(len(coords), size=PATCHES_PER_IMAGE, replace=False)
        for number, position in enumerate(selected, start=1):
            y, x = coords[int(position)]
            patch = image[y : y + ph, x : x + pw]
            patches.append(patch)
            names.append(f"{source_name}_{number:02d}")
    return patches, names


def save_segmentation(name: str, original: np.ndarray, segmented: np.ndarray) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    axes[0].imshow(original)
    axes[0].set_title("Вхідне зображення")
    axes[1].imshow(segmented)
    axes[1].set_title(f"K-means сегментація, K={SEGMENT_CLUSTERS}")
    for axis in axes:
        axis.axis("off")
    fig.tight_layout()
    fig.savefig(RESULTS / f"segmentation_{name}.png", dpi=170)
    plt.close(fig)


def save_cluster_montage(
    patches: list[np.ndarray], names: list[str], labels: np.ndarray
) -> None:
    fig, axes = plt.subplots(3, 4, figsize=(12, 8))
    for index, axis in enumerate(axes.ravel()):
        axis.imshow(patches[index])
        axis.set_title(f"{names[index]} | кластер {labels[index] + 1}", fontsize=9)
        axis.axis("off")
    fig.suptitle("Кластеризація 12 фрагментів даних ДЗЗ", fontsize=14)
    fig.tight_layout()
    fig.savefig(RESULTS / "patch_clusters.png", dpi=180)
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    images = [
        ("landsat", load_rgb(SOURCE / "landsat.png")),
        ("bing", load_rgb(SOURCE / "bing.png")),
    ]

    for name, image in images:
        small, segmented = segment(image)
        Image.fromarray(segmented).save(RESULTS / f"{name}_segmented.png")
        save_segmentation(name, small, segmented)

    patches, names = build_dataset(images)
    features = np.vstack([patch_features(patch) for patch in patches])
    normalized = (features - features.mean(0)) / (features.std(0) + 1e-9)
    centers, labels = kmeans(normalized, SCENE_CLUSTERS, iterations=100)
    save_cluster_montage(patches, names, labels)

    with (RESULTS / "clusters.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["sample", "cluster", "feature_distance"])
        for name, label, vector in zip(names, labels, normalized):
            distance = float(np.linalg.norm(vector - centers[label]))
            writer.writerow([name, int(label + 1), f"{distance:.5f}"])

    counts = np.bincount(labels, minlength=SCENE_CLUSTERS)
    print("Кластеризацію завершено")
    print("Розподіл 12 фрагментів:", counts.tolist())
    print("Результати:", RESULTS)


if __name__ == "__main__":
    main()
