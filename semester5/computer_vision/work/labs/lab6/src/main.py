from __future__ import annotations

import csv
from collections import deque
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
RESULTS = PROJECT / "results"

WIDTH, HEIGHT = 640, 360
FRAME_COUNT = 72
MOTION_THRESHOLD = 35
MIN_COMPONENT_AREA = 90


def background() -> np.ndarray:
    image = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    image[:] = (170, 205, 225)
    image[245:] = (72, 120, 70)
    image[270:340] = (75, 78, 82)
    image[302:308, ::2] = (230, 220, 110)
    return image


def generate_frame(index: int) -> tuple[np.ndarray, list[tuple[str, tuple[int, int, int, int]]]]:
    canvas = Image.fromarray(background())
    draw = ImageDraw.Draw(canvas)
    truth: list[tuple[str, tuple[int, int, int, int]]] = []

    # Автомобіль: широкий прямокутний об'єкт.
    car_x = -120 + index * 10
    car_box = (car_x, 278, car_x + 108, 326)
    draw.rounded_rectangle(car_box, radius=9, fill=(205, 45, 45), outline=(90, 15, 15), width=3)
    draw.ellipse((car_x + 14, 314, car_x + 34, 334), fill=(25, 25, 25))
    draw.ellipse((car_x + 74, 314, car_x + 94, 334), fill=(25, 25, 25))
    truth.append(("автомобіль", car_box))

    # Людина: вузький високий об'єкт.
    person_x = 520 - index * 5
    person_box = (person_x, 185, person_x + 28, 270)
    draw.ellipse((person_x + 5, 185, person_x + 23, 203), fill=(245, 195, 70))
    draw.rectangle((person_x + 8, 204, person_x + 20, 247), fill=(45, 75, 190))
    draw.line((person_x + 11, 246, person_x + 5, 270), fill=(30, 30, 30), width=5)
    draw.line((person_x + 18, 246, person_x + 25, 270), fill=(30, 30, 30), width=5)
    truth.append(("людина", person_box))

    # М'яч: невеликий майже квадратний компонент.
    ball_x = 80 + index * 6
    ball_y = 235 - round(55 * abs(np.sin(index / 10)))
    ball_box = (ball_x, ball_y, ball_x + 22, ball_y + 22)
    draw.ellipse(ball_box, fill=(245, 220, 40), outline=(110, 90, 0), width=2)
    truth.append(("м'яч", ball_box))
    return np.asarray(canvas), truth


def motion_mask(frame: np.ndarray, reference: np.ndarray) -> np.ndarray:
    difference = np.abs(frame.astype(np.int16) - reference.astype(np.int16)).max(axis=2)
    mask = difference > MOTION_THRESHOLD
    # Морфологічне замикання 3x3 у спрощеній реалізації.
    padded = np.pad(mask, 1)
    dilated = np.zeros_like(mask)
    for dy in range(3):
        for dx in range(3):
            dilated |= padded[dy : dy + HEIGHT, dx : dx + WIDTH]
    padded = np.pad(dilated, 1, constant_values=True)
    eroded = np.ones_like(mask)
    for dy in range(3):
        for dx in range(3):
            eroded &= padded[dy : dy + HEIGHT, dx : dx + WIDTH]
    return eroded


def connected_components(mask: np.ndarray) -> list[tuple[int, int, int, int, int]]:
    visited = np.zeros_like(mask, dtype=bool)
    components: list[tuple[int, int, int, int, int]] = []
    for y, x in zip(*np.nonzero(mask & ~visited)):
        if visited[y, x]:
            continue
        queue = deque([(int(y), int(x))])
        visited[y, x] = True
        points: list[tuple[int, int]] = []
        while queue:
            cy, cx = queue.popleft()
            points.append((cy, cx))
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < HEIGHT and 0 <= nx < WIDTH and mask[ny, nx] and not visited[ny, nx]:
                    visited[ny, nx] = True
                    queue.append((ny, nx))
        if len(points) >= MIN_COMPONENT_AREA:
            ys, xs = np.asarray(points).T
            components.append((int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1), len(points)))
    return components


def classify(box: tuple[int, int, int, int, int]) -> str:
    x1, y1, x2, y2, area = box
    width, height = x2 - x1, y2 - y1
    aspect = width / max(height, 1)
    # Ієрархія: рух -> геометричний компонент -> клас за формою та площею.
    if y1 >= 270 and area > 500:
        return "автомобіль"
    if aspect < 0.75 and height > 55:
        return "людина"
    if 0.65 <= aspect <= 1.45 and area < 900:
        return "м'яч"
    return "інший"


def annotate(frame: np.ndarray, detections: list[tuple[str, tuple[int, int, int, int, int]]]) -> Image.Image:
    image = Image.fromarray(frame)
    draw = ImageDraw.Draw(image)
    colors = {"автомобіль": "#00ff66", "людина": "#00d9ff", "м'яч": "#ffe000", "інший": "#ff66cc"}
    labels_ascii = {"автомобіль": "CAR", "людина": "PERSON", "м'яч": "BALL", "інший": "OTHER"}
    for label, (x1, y1, x2, y2, _) in detections:
        draw.rectangle((x1, y1, x2, y2), outline=colors[label], width=3)
        draw.text((x1 + 2, max(2, y1 - 14)), labels_ascii[label], fill=colors[label])
    return image


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    reference = background()
    annotated_frames: list[Image.Image] = []
    rows: list[list[object]] = []
    total_expected = total_correct = 0

    for frame_index in range(FRAME_COUNT):
        frame, truth = generate_frame(frame_index)
        mask = motion_mask(frame, reference)
        boxes = connected_components(mask)
        detections = [(classify(box), box) for box in boxes]
        annotated_frames.append(annotate(frame, detections))

        expected = {label for label, box in truth if box[2] > 0 and box[0] < WIDTH}
        found = {label for label, _ in detections}
        total_expected += len(expected)
        total_correct += len(expected & found)
        rows.append([frame_index, ";".join(sorted(expected)), ";".join(sorted(found)), len(boxes)])

    annotated_frames[0].save(
        RESULTS / "tracking.gif",
        save_all=True,
        append_images=annotated_frames[1:],
        duration=55,
        loop=0,
        optimize=True,
    )

    selected = [0, 18, 36, 54, 71]
    fig, axes = plt.subplots(1, 5, figsize=(15, 3.6))
    for axis, index in zip(axes, selected):
        axis.imshow(annotated_frames[index])
        axis.set_title(f"Кадр {index}")
        axis.axis("off")
    fig.suptitle("Ієрархічна ідентифікація динамічних об'єктів")
    fig.tight_layout()
    fig.savefig(RESULTS / "tracking_montage.png", dpi=170)
    plt.close(fig)

    with (RESULTS / "detections.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["frame", "expected_classes", "detected_classes", "components"])
        writer.writerows(rows)

    recall = total_correct / max(total_expected, 1)
    print(f"Кадрів: {FRAME_COUNT}")
    print(f"Повнота ідентифікації класів: {recall:.4f}")
    print("Результати:", RESULTS)


if __name__ == "__main__":
    main()
