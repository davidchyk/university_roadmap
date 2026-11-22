from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
RESULTS = PROJECT / "results"
DATASET = RESULTS / "dataset"

FRAME_COUNT = 42
FPS = 12


def cuboid_faces(center: tuple[float, float, float], size: tuple[float, float, float]) -> list[list[tuple[float, float, float]]]:
    cx, cy, cz = center
    sx, sy, sz = np.asarray(size) / 2
    vertices = [
        (cx + dx * sx, cy + dy * sy, cz + dz * sz)
        for dx in (-1, 1)
        for dy in (-1, 1)
        for dz in (-1, 1)
    ]
    return [
        [vertices[i] for i in face]
        for face in ([0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5])
    ]


def add_cuboid(axis, center, size, color, edge="black", alpha=1.0) -> None:
    collection = Poly3DCollection(cuboid_faces(center, size), facecolors=color, edgecolors=edge, linewidths=0.45, alpha=alpha)
    axis.add_collection3d(collection)


def add_vehicle(axis, x: float, y: float, turret_angle: float) -> None:
    # Гусениці, корпус, башта.
    add_cuboid(axis, (x, y - 0.85, 0.42), (3.8, 0.42, 0.62), "#202522")
    add_cuboid(axis, (x, y + 0.85, 0.42), (3.8, 0.42, 0.62), "#202522")
    add_cuboid(axis, (x, y, 0.92), (3.5, 1.55, 0.72), "#c6a548")
    add_cuboid(axis, (x - 0.15, y, 1.52), (1.45, 1.15, 0.52), "#e0bd57")

    # Катки як темні диски на обох боках.
    for offset in np.linspace(-1.35, 1.35, 5):
        for side in (-1.08, 1.08):
            theta = np.linspace(0, 2 * np.pi, 24)
            axis.plot(x + offset + 0.27 * np.cos(theta), np.full_like(theta, y + side), 0.38 + 0.27 * np.sin(theta), color="#171817", linewidth=2.2)

    # Гармата повертається разом із баштою.
    length = 2.7
    dx, dy = length * np.cos(turret_angle), length * np.sin(turret_angle)
    axis.plot([x + 0.35 * np.cos(turret_angle), x + dx], [y + 0.35 * np.sin(turret_angle), y + dy], [1.65, 1.65], color="#2b2f28", linewidth=7, solid_capstyle="round")


def render_frame(index: int) -> tuple[Image.Image, dict[str, float]]:
    progress = index / (FRAME_COUNT - 1)
    x = -6.2 + 12.4 * progress
    y = 0.65 * np.sin(progress * 2 * np.pi)
    turret_angle = 0.35 * np.sin(progress * 4 * np.pi)

    fig = plt.figure(figsize=(8, 5.2), dpi=100)
    canvas = FigureCanvasAgg(fig)
    axis = fig.add_subplot(111, projection="3d")

    # Земля, дорога, розмітка та статичні перешкоди.
    gx, gy = np.meshgrid(np.linspace(-8, 8, 2), np.linspace(-5, 5, 2))
    axis.plot_surface(gx, gy, np.zeros_like(gx), color="#718e5d", shade=False, alpha=0.32)
    rx, ry = np.meshgrid(np.linspace(-8, 8, 2), np.linspace(-1.7, 1.7, 2))
    axis.plot_surface(rx, ry, np.full_like(rx, 0.015), color="#676b6c", shade=False, alpha=0.55)
    axis.plot([-8, 8], [0, 0], [0.025, 0.025], color="#f2df7a", linewidth=2, linestyle="--")
    add_cuboid(axis, (4.7, 3.2, 0.8), (1.1, 1.1, 1.6), "#9b835e")
    add_cuboid(axis, (-3.8, -3.4, 0.6), (1.4, 1.1, 1.2), "#856d4a")
    add_vehicle(axis, x, y, turret_angle)

    axis.set_xlim(-8, 8)
    axis.set_ylim(-5, 5)
    axis.set_zlim(0, 4.2)
    axis.set_box_aspect((16, 10, 5))
    axis.view_init(elev=24, azim=-58 + 8 * np.sin(progress * 2 * np.pi))
    axis.set(xlabel="X", ylabel="Y", zlabel="Z", title=f"Динамічна 3D-модель бронетехніки — кадр {index:02d}")
    fig.tight_layout()
    canvas.draw()
    rgba = np.asarray(canvas.buffer_rgba()).copy()
    plt.close(fig)
    return Image.fromarray(rgba[..., :3]), {"x": x, "y": y, "turret_angle_rad": turret_angle}


def main() -> None:
    DATASET.mkdir(parents=True, exist_ok=True)
    frames: list[Image.Image] = []
    metadata: list[list[object]] = []
    for index in range(FRAME_COUNT):
        frame, pose = render_frame(index)
        frame.save(DATASET / f"frame_{index:03d}.jpg", quality=90, optimize=True)
        frames.append(frame.resize((640, 416), Image.Resampling.LANCZOS))
        metadata.append([index, f"{pose['x']:.5f}", f"{pose['y']:.5f}", f"{pose['turret_angle_rad']:.5f}", "armored_vehicle"])

    frames[0].save(
        RESULTS / "armored_vehicle.gif",
        save_all=True,
        append_images=frames[1:],
        duration=round(1000 / FPS),
        loop=0,
        optimize=True,
    )

    selected = [0, 10, 20, 30, 41]
    fig, axes = plt.subplots(1, 5, figsize=(15, 3.2))
    for axis, index in zip(axes, selected):
        axis.imshow(frames[index])
        axis.set_title(f"Кадр {index}")
        axis.axis("off")
    fig.suptitle("Рух бронетехніки у синтезованій 3D-сцені")
    fig.tight_layout()
    fig.savefig(RESULTS / "scene_montage.png", dpi=170)
    plt.close(fig)

    with (RESULTS / "dataset_labels.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["frame", "x", "y", "turret_angle_rad", "class"])
        writer.writerows(metadata)

    print(f"Створено {FRAME_COUNT} кадри набору даних")
    print(f"Тривалість анімації: {FRAME_COUNT / FPS:.2f} с")
    print("Результати:", RESULTS)


if __name__ == "__main__":
    main()
