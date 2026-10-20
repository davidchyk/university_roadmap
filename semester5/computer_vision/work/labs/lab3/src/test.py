"""Експеримент із foundation-моделлю Segment Anything (SAM).

Скрипт не навчає модель: SAM генерує маски об'єктів, а простий геометричний
фільтр залишає великі компактні області, схожі на дахи. SAM не є спеціальною
моделлю будівель, тому результат треба сприймати як демонстрацію технології,
а не як гарантований автоматичний підрахунок будівель.

Приклад:
    python test.py --checkpoint sam_vit_b_01ec64.pth \
        --image landsat.png --output sam_result.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SAM building-mask experiment")
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--image", type=Path, default=Path("landsat.png"))
    parser.add_argument("--output", type=Path, default=Path("sam_result.png"))
    parser.add_argument("--model-type", choices=("vit_b", "vit_l", "vit_h"), default="vit_b")
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    return parser.parse_args()


def choose_device(requested: str) -> str:
    import torch

    if requested == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA запитано, але CUDA недоступна")
        return "cuda"
    if requested == "cpu":
        return "cpu"
    return "cuda" if torch.cuda.is_available() else "cpu"


def bbox_iou(first: tuple[int, int, int, int], second: tuple[int, int, int, int]) -> float:
    ax, ay, aw, ah = first
    bx, by, bw, bh = second
    x1, y1 = max(ax, bx), max(ay, by)
    x2, y2 = min(ax + aw, bx + bw), min(ay + ah, by + bh)
    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    union = aw * ah + bw * bh - intersection
    return intersection / union if union else 0.0


def looks_like_roof(mask: np.ndarray, image: np.ndarray) -> tuple[bool, float, tuple[int, int, int, int]]:
    height, width = mask.shape
    image_area = height * width
    area = int(mask.sum())
    x, y, box_width, box_height = cv2.boundingRect(mask.astype(np.uint8))
    ratio = area / image_area
    aspect = box_width / max(box_height, 1)
    extent = area / max(box_width * box_height, 1)
    contour, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contour:
        return False, 0.0, (x, y, box_width, box_height)
    contour = max(contour, key=cv2.contourArea)
    contour_area = max(cv2.contourArea(contour), 1.0)
    hull_area = max(cv2.contourArea(cv2.convexHull(contour)), 1.0)
    solidity = contour_area / hull_area

    # Будівлі не повинні бути обрізані краєм кадру.
    touches_border = x <= 1 or y <= 1 or x + box_width >= width - 1 or y + box_height >= height - 1
    if not 0.00035 <= ratio <= 0.08 or touches_border:
        return False, 0.0, (x, y, box_width, box_height)
    if not 0.18 <= aspect <= 5.5 or extent < 0.28 or solidity < 0.60:
        return False, 0.0, (x, y, box_width, box_height)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mean_saturation = float(hsv[:, :, 1][mask].mean()) / 255.0
    mean_value = float(hsv[:, :, 2][mask].mean()) / 255.0
    # Це слабка ознака даху, а не семантичний класифікатор.
    color_score = max(0.0, 1.0 - mean_saturation) * 0.6 + mean_value * 0.4
    score = 0.35 * min(extent, 1.0) + 0.35 * solidity + 0.30 * color_score
    return True, score, (x, y, box_width, box_height)


def non_maximum_suppression(candidates: list[dict], threshold: float = 0.45) -> list[dict]:
    selected: list[dict] = []
    for candidate in sorted(candidates, key=lambda item: item["score"], reverse=True):
        if all(bbox_iou(candidate["bbox"], other["bbox"]) < threshold for other in selected):
            selected.append(candidate)
    return selected


def main() -> None:
    args = parse_args()
    try:
        from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
    except ImportError as error:
        raise SystemExit(
            "Не встановлено segment-anything. Встанови залежності з requirements-sam.txt."
        ) from error

    image = cv2.imread(str(args.image), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити зображення: {args.image}")
    if not args.checkpoint.exists():
        raise FileNotFoundError(f"Не знайдено checkpoint SAM: {args.checkpoint}")

    device = choose_device(args.device)
    model = sam_model_registry[args.model_type](checkpoint=str(args.checkpoint))
    model.to(device=device)
    generator = SamAutomaticMaskGenerator(
        model,
        points_per_side=32,
        pred_iou_thresh=0.86,
        stability_score_thresh=0.90,
        crop_n_layers=1,
        min_mask_region_area=700,
    )

    masks = generator.generate(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    candidates = []
    for mask_data in masks:
        mask = mask_data["segmentation"]
        accepted, score, bbox = looks_like_roof(mask, image)
        if accepted:
            candidates.append({"mask": mask, "score": score, "bbox": bbox})
    candidates = non_maximum_suppression(candidates)

    result = image.copy()
    for index, candidate in enumerate(candidates, start=1):
        mask = candidate["mask"]
        x, y, box_width, box_height = candidate["bbox"]
        color = (0, 220, 255)
        result[mask] = (0.65 * result[mask] + 0.35 * np.array(color)).astype(np.uint8)
        cv2.rectangle(result, (x, y), (x + box_width, y + box_height), (0, 0, 255), 2)
        cv2.putText(result, str(index), (x + 4, y + 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 0, 0), 2, cv2.LINE_AA)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.output), result)
    print(f"SAM masks: {len(masks)}")
    print(f"Roof-like candidates after filtering: {len(candidates)}")
    print(f"Device: {device}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
