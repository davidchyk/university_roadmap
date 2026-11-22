from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
RESULTS = PROJECT / "results"
RNG = np.random.default_rng(4106)

WIDTH, HEIGHT = 640, 480
FOCAL_LENGTH = 520.0
BASELINE = 0.22
CX, CY = WIDTH / 2, HEIGHT / 2
POINTS_PER_FACE = 500
PIXEL_NOISE = 0.18


def sample_face(axis: int, value: float, count: int) -> np.ndarray:
    points = RNG.uniform(-1.0, 1.0, size=(count, 3))
    points[:, axis] = value
    return points


def create_object() -> np.ndarray:
    """Хмара точок поверхні асиметричного 3D-об'єкта."""
    cube = np.vstack([sample_face(axis, side, POINTS_PER_FACE) for axis in range(3) for side in (-1.0, 1.0)])
    cube[:, 0] *= 1.15
    cube[:, 1] *= 0.8
    cube[:, 2] *= 0.7
    cube[:, 2] += 5.2

    # Верхня піраміда робить форму несиметричною і наочною.
    t = RNG.random((1400, 1))
    angle = RNG.uniform(0, 2 * np.pi, size=(1400, 1))
    radius = (1 - t) * 0.75
    pyramid = np.column_stack(
        [
            (radius * np.cos(angle)).ravel(),
            (radius * np.sin(angle)).ravel(),
            (5.9 + t * 1.25).ravel(),
        ]
    )
    return np.vstack([cube, pyramid])


def project(points: np.ndarray, camera_x: float) -> np.ndarray:
    relative = points.copy()
    relative[:, 0] -= camera_x
    u = FOCAL_LENGTH * relative[:, 0] / relative[:, 2] + CX
    v = FOCAL_LENGTH * relative[:, 1] / relative[:, 2] + CY
    return np.column_stack([u, v])


def render(points: np.ndarray, pixels: np.ndarray) -> np.ndarray:
    image = np.full((HEIGHT, WIDTH, 3), 242, dtype=np.uint8)
    depth = points[:, 2]
    colors = plt.get_cmap("viridis")((depth - depth.min()) / np.ptp(depth))[:, :3]
    order = np.argsort(depth)[::-1]
    for index in order:
        u, v = np.rint(pixels[index]).astype(int)
        if 2 <= u < WIDTH - 2 and 2 <= v < HEIGHT - 2:
            image[v - 2 : v + 3, u - 2 : u + 3] = (colors[index] * 255).astype(np.uint8)
    return image


def reconstruct(left: np.ndarray, right: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    noisy_left = left + RNG.normal(0, PIXEL_NOISE, left.shape)
    noisy_right = right + RNG.normal(0, PIXEL_NOISE, right.shape)
    disparity = noisy_left[:, 0] - noisy_right[:, 0]
    z = FOCAL_LENGTH * BASELINE / disparity
    x = (noisy_left[:, 0] - CX) * z / FOCAL_LENGTH - BASELINE / 2
    y = (noisy_left[:, 1] - CY) * z / FOCAL_LENGTH
    return np.column_stack([x, y, z]), disparity


def save_results(
    points: np.ndarray,
    reconstructed: np.ndarray,
    left_image: np.ndarray,
    right_image: np.ndarray,
    left_pixels: np.ndarray,
    disparity: np.ndarray,
) -> None:
    Image.fromarray(left_image).save(RESULTS / "left_camera.png")
    Image.fromarray(right_image).save(RESULTS / "right_camera.png")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].imshow(left_image)
    axes[0].set_title("Ліва віртуальна камера")
    axes[1].imshow(right_image)
    axes[1].set_title("Права віртуальна камера")
    for axis in axes:
        axis.axis("off")
    fig.suptitle(f"Стереопара, базис B={BASELINE:.2f} м")
    fig.tight_layout()
    fig.savefig(RESULTS / "stereo_pair.png", dpi=180)
    plt.close(fig)

    disparity_image = np.zeros((HEIGHT, WIDTH), dtype=float)
    counts = np.zeros((HEIGHT, WIDTH), dtype=int)
    for (u, v), value in zip(np.rint(left_pixels).astype(int), disparity):
        if 0 <= u < WIDTH and 0 <= v < HEIGHT:
            disparity_image[v, u] += value
            counts[v, u] += 1
    valid = counts > 0
    disparity_image[valid] /= counts[valid]
    fig, axis = plt.subplots(figsize=(8, 5))
    image = axis.imshow(disparity_image, cmap="magma", vmin=disparity.min(), vmax=disparity.max())
    axis.set_title("Карта диспаритету")
    axis.axis("off")
    fig.colorbar(image, ax=axis, label="d, пікселі")
    fig.tight_layout()
    fig.savefig(RESULTS / "disparity_map.png", dpi=180)
    plt.close(fig)

    sample = RNG.choice(len(points), size=2800, replace=False)
    fig = plt.figure(figsize=(12, 5.5))
    ax1 = fig.add_subplot(121, projection="3d")
    ax2 = fig.add_subplot(122, projection="3d")
    for axis, cloud, title in [
        (ax1, points, "Вихідна 3D-модель"),
        (ax2, reconstructed, "Реконструйована хмара точок"),
    ]:
        axis.scatter(cloud[sample, 0], cloud[sample, 1], cloud[sample, 2], c=cloud[sample, 2], cmap="viridis", s=3)
        axis.set(xlabel="X, м", ylabel="Y, м", zlabel="Z, м", title=title)
        axis.view_init(elev=22, azim=-58)
        axis.set_box_aspect((1, 0.8, 1))
    fig.tight_layout()
    fig.savefig(RESULTS / "reconstruction.png", dpi=190)
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    points = create_object()
    left_pixels = project(points, -BASELINE / 2)
    right_pixels = project(points, BASELINE / 2)
    left_image = render(points, left_pixels)
    right_image = render(points, right_pixels)
    reconstructed, disparity = reconstruct(left_pixels, right_pixels)
    save_results(points, reconstructed, left_image, right_image, left_pixels, disparity)

    errors = np.linalg.norm(points - reconstructed, axis=1)
    with (RESULTS / "metrics.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["metric", "value"])
        writer.writerow(["points", len(points)])
        writer.writerow(["focal_length_px", FOCAL_LENGTH])
        writer.writerow(["baseline_m", BASELINE])
        writer.writerow(["mean_error_m", f"{errors.mean():.6f}"])
        writer.writerow(["rmse_m", f"{np.sqrt(np.mean(errors ** 2)):.6f}"])
        writer.writerow(["p95_error_m", f"{np.percentile(errors, 95):.6f}"])

    print(f"Точок: {len(points)}")
    print(f"Середня похибка реконструкції: {errors.mean():.4f} м")
    print(f"RMSE: {np.sqrt(np.mean(errors ** 2)):.4f} м")
    print("Результати:", RESULTS)


if __name__ == "__main__":
    main()
