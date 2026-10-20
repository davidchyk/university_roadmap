from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
SRC_DIR = ROOT
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Змінювані параметри лабораторної роботи.
BLUR_KERNEL = (5, 5)
CLAHE_CLIP_LIMIT = 2.0
CLAHE_GRID_SIZE = (8, 8)
MORPH_KERNEL = (5, 5)
MIN_AREA_RATIO = 0.00020
MAX_AREA_RATIO = 0.035
MIN_ASPECT = 0.18
MAX_ASPECT = 5.50
MIN_EXTENT = 0.28
MIN_SOLIDITY = 0.55
MIN_RECTANGULARITY = 0.18
REJECT_BORDER = True
REGISTERED_RATIO_TEST = 0.75
REGISTERED_RANSAC_THRESHOLD = 5.0
REGISTERED_MIN_AREA_RATIO = 0.00020
REGISTERED_MIN_EXTENT = 0.28
REGISTERED_MIN_SOLIDITY = 0.65
REGISTERED_MIN_RECTANGULARITY = 0.18


@dataclass(frozen=True)
class Detection:
    contour: np.ndarray
    area: float
    bbox: tuple[int, int, int, int]
    center: tuple[int, int]
    score: float


def load_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Не вдалося завантажити зображення: {path}")
    return image


def preprocess(image: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(CLAHE_CLIP_LIMIT, CLAHE_GRID_SIZE)
    enhanced = clahe.apply(gray)
    blurred = cv2.GaussianBlur(enhanced, BLUR_KERNEL, 0)
    return gray, enhanced, blurred


def build_masks(image: np.ndarray) -> dict[str, np.ndarray]:
    gray, enhanced, blurred = preprocess(image)

    _, otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    adaptive = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 4,
    )

    edges = cv2.Canny(blurred, 45, 135)
    edge_mask = cv2.morphologyEx(
        edges, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_RECT, MORPH_KERNEL),
    )

    # Світлі малонасичені області часто відповідають поверхням дахів.
    b, g, r = cv2.split(image.astype(np.int16))
    neutral = (
        (np.abs(r - g) <= 28)
        & (np.abs(g - b) <= 28)
        & (r >= 105) & (g >= 105) & (b >= 105)
    ).astype(np.uint8) * 255
    color_mask = cv2.morphologyEx(
        neutral, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)),
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, MORPH_KERNEL)
    masks = {}
    for name, mask in {
        "otsu": otsu,
        "adaptive": adaptive,
        "edges": edge_mask,
        "color": color_mask,
    }.items():
        cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
        masks[name] = cleaned

    # Комбінація двох незалежних ознак: яскравість/текстура та колір.
    masks["otsu_color"] = cv2.bitwise_and(masks["otsu"], masks["color"])
    masks["adaptive_color"] = cv2.bitwise_and(masks["adaptive"], masks["color"])
    masks["gray_consensus"] = cv2.bitwise_or(masks["otsu"], masks["adaptive"])
    masks["enhanced_gray"] = enhanced
    masks["gray"] = gray
    return masks


def contour_features(contour: np.ndarray, shape: tuple[int, ...]) -> Detection | None:
    height, width = shape[:2]
    image_area = float(height * width)
    area = float(cv2.contourArea(contour))
    x, y, w, h = cv2.boundingRect(contour)
    if area < image_area * MIN_AREA_RATIO or area > image_area * MAX_AREA_RATIO:
        return None
    if REJECT_BORDER and (x <= 1 or y <= 1 or x + w >= width - 1 or y + h >= height - 1):
        return None
    aspect = w / max(h, 1)
    extent = area / max(w * h, 1)
    hull = cv2.convexHull(contour)
    hull_area = max(cv2.contourArea(hull), 1.0)
    solidity = area / hull_area
    perimeter = max(cv2.arcLength(contour, True), 1.0)
    rectangularity = (4.0 * np.pi * area) / (perimeter * perimeter)
    if not MIN_ASPECT <= aspect <= MAX_ASPECT:
        return None
    if extent < MIN_EXTENT or solidity < MIN_SOLIDITY or rectangularity < MIN_RECTANGULARITY:
        return None
    moments = cv2.moments(contour)
    if moments["m00"]:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
    else:
        cx, cy = x + w // 2, y + h // 2
    score = 0.35 * min(extent, 1.0) + 0.35 * solidity + 0.30 * min(rectangularity, 1.0)
    return Detection(contour, area, (x, y, w, h), (cx, cy), score)


def detect(mask: np.ndarray, image_shape: tuple[int, ...]) -> list[Detection]:
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detections = [item for c in contours if (item := contour_features(c, image_shape))]
    return sorted(detections, key=lambda d: d.area, reverse=True)


def draw_detections(image: np.ndarray, detections: list[Detection]) -> np.ndarray:
    result = image.copy()
    for index, detection in enumerate(detections, start=1):
        x, y, w, h = detection.bbox
        cv2.drawContours(result, [detection.contour], -1, (0, 220, 255), 2)
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.putText(result, str(index), (detection.center[0] - 8, detection.center[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 0, 0), 2, cv2.LINE_AA)
    return result


def save_image(path: Path, image: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)


def estimate_homography(source: np.ndarray, target: np.ndarray) -> tuple[np.ndarray | None, int]:
    """Оцінює H, яка переводить координати source у координати target."""
    source_gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(nfeatures=4000)
    source_keypoints, source_descriptors = orb.detectAndCompute(source_gray, None)
    target_keypoints, target_descriptors = orb.detectAndCompute(target_gray, None)
    if source_descriptors is None or target_descriptors is None:
        return None, 0
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    pairs = matcher.knnMatch(source_descriptors, target_descriptors, k=2)
    good = [first for first, second in pairs if first.distance < REGISTERED_RATIO_TEST * second.distance]
    if len(good) < 4:
        return None, len(good)
    source_points = np.float32([source_keypoints[m.queryIdx].pt for m in good])
    target_points = np.float32([target_keypoints[m.trainIdx].pt for m in good])
    homography, inlier_mask = cv2.findHomography(
        source_points, target_points, cv2.RANSAC, REGISTERED_RANSAC_THRESHOLD
    )
    if homography is None or inlier_mask is None:
        return None, 0
    return homography, int(inlier_mask.sum())


def registered_consensus(
    reference: np.ndarray, second: np.ndarray,
) -> tuple[np.ndarray, np.ndarray | None, int]:
    """Повертає перетин нейтральних масок після геометричного вирівнювання."""
    reference_masks = build_masks(reference)
    second_masks = build_masks(second)
    homography, inliers = estimate_homography(second, reference)
    if homography is None:
        return np.zeros(reference.shape[:2], dtype=np.uint8), None, inliers
    height, width = reference.shape[:2]
    warped = cv2.warpPerspective(
        second_masks["color"], homography, (width, height), flags=cv2.INTER_NEAREST
    )
    valid = cv2.warpPerspective(
        np.full(second.shape[:2], 255, dtype=np.uint8), homography, (width, height),
        flags=cv2.INTER_NEAREST,
    )
    stable = cv2.bitwise_and(reference_masks["color"], warped)
    stable = cv2.bitwise_and(stable, valid)
    stable = cv2.morphologyEx(
        stable, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)),
    )
    return stable, homography, inliers


def detect_registered(mask: np.ndarray, image: np.ndarray) -> list[Detection]:
    """Фільтрація зі строгішими ознаками стабільного результату."""
    global MIN_AREA_RATIO, MIN_EXTENT, MIN_SOLIDITY, MIN_RECTANGULARITY
    old = MIN_AREA_RATIO, MIN_EXTENT, MIN_SOLIDITY, MIN_RECTANGULARITY
    MIN_AREA_RATIO = REGISTERED_MIN_AREA_RATIO
    MIN_EXTENT = REGISTERED_MIN_EXTENT
    MIN_SOLIDITY = REGISTERED_MIN_SOLIDITY
    MIN_RECTANGULARITY = REGISTERED_MIN_RECTANGULARITY
    try:
        return detect(mask, image.shape)
    finally:
        MIN_AREA_RATIO, MIN_EXTENT, MIN_SOLIDITY, MIN_RECTANGULARITY = old


def process_image(name: str, path: Path) -> list[dict[str, object]]:
    image = load_image(path)
    masks = build_masks(image)
    output_dir = RESULTS_DIR / name
    output_dir.mkdir(parents=True, exist_ok=True)
    save_image(output_dir / "original.png", image)
    save_image(output_dir / "grayscale.png", masks["gray"])
    save_image(output_dir / "enhanced.png", masks["enhanced_gray"])

    rows = []
    for method, mask in masks.items():
        if method in {"gray", "enhanced_gray"}:
            continue
        detections = detect(mask, image.shape)
        save_image(output_dir / f"mask_{method}.png", mask)
        save_image(output_dir / f"detected_{method}.png", draw_detections(image, detections))
        rows.append({"image": name, "method": method, "count": len(detections)})

    # Основний результат: об'єднуємо найбільш стабільні маски та прибираємо шум.
    main_mask = cv2.bitwise_or(masks["otsu_color"], masks["adaptive_color"])
    main_mask = cv2.morphologyEx(
        main_mask, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)),
    )
    detections = detect(main_mask, image.shape)
    save_image(output_dir / "mask_final.png", main_mask)
    save_image(output_dir / "detected_final.png", draw_detections(image, detections))
    rows.append({"image": name, "method": "combined", "count": len(detections)})
    return rows


def main() -> None:
    inputs = {
        "landsat": SRC_DIR / "landsat.png",
        "bing": SRC_DIR / "bing.png",
    }
    missing = [str(path) for path in inputs.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Відсутні вхідні зображення: " + ", ".join(missing))

    rows = []
    for name, path in inputs.items():
        rows.extend(process_image(name, path))

    reference = load_image(inputs["landsat"])
    second = load_image(inputs["bing"])
    stable_mask, homography, inliers = registered_consensus(reference, second)
    if homography is not None:
        stable_detections = detect_registered(stable_mask, reference)
        registered_dir = RESULTS_DIR / "registered"
        registered_dir.mkdir(parents=True, exist_ok=True)
        warped_second = cv2.warpPerspective(
            second, homography, (reference.shape[1], reference.shape[0])
        )
        save_image(registered_dir / "bing_warped_to_landsat.png", warped_second)
        save_image(registered_dir / "stable_mask.png", stable_mask)
        save_image(registered_dir / "stable_result.png", draw_detections(reference, stable_detections))
        rows.append({"image": "registered", "method": "stable_consensus", "count": len(stable_detections)})
        print(f"registered stable consensus: {len(stable_detections)} objects, {inliers} ORB inliers")
    with (RESULTS_DIR / "summary.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["image", "method", "count"])
        writer.writeheader()
        writer.writerows(rows)
    print("Обробку завершено. Зведення:")
    for row in rows:
        if row["method"] in {"combined", "stable_consensus"}:
            print(f"{row['image']}: {row['count']} об'єктів")


if __name__ == "__main__":
    main()
