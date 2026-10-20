from itertools import product
from pathlib import Path

import cv2
import numpy as np

import main


def evaluate(image: np.ndarray, mask: np.ndarray, params: tuple[float, float, float, float]):
    main.MIN_AREA_RATIO, main.MIN_EXTENT, main.MIN_SOLIDITY, main.MIN_RECTANGULARITY = params
    detections = main.detect(mask, image.shape)
    if not detections:
        return None
    areas = np.array([item.area / (image.shape[0] * image.shape[1]) for item in detections])
    # Перевага надається результатам із достатньою кількістю великих,
    # компактних областей, а не набором дрібних фрагментів.
    quality = float(np.mean(areas >= 0.0008) - 0.25 * np.mean(areas <= 0.0012))
    return detections, quality


def main_search() -> None:
    values = list(product(
        [0.00020, 0.00035, 0.00050, 0.00075, 0.00100],
        [0.28, 0.38, 0.48, 0.58],
        [0.55, 0.65, 0.75],
        [0.18, 0.26, 0.34],
    ))
    for name in ("landsat", "bing"):
        image = main.load_image(main.SRC_DIR / f"{name}.png")
        masks = main.build_masks(image)
        if name == "landsat":
            registered = cv2.imread(
                str(main.PROJECT_ROOT.parent / "lab2" / "results" / "registered_pair" / "registered_color_consensus_mask.png"),
                cv2.IMREAD_GRAYSCALE,
            )
            if registered is not None:
                masks["registered_consensus"] = registered
        rows = []
        for method in ("color", "otsu", "adaptive_color", "registered_consensus"):
            if method not in masks:
                continue
            for params in values:
                result = evaluate(image, masks[method], params)
                if result is None:
                    continue
                detections, quality = result
                rows.append((abs(len(detections) - 25) - quality, method, params, len(detections), quality, detections))
        rows.sort(key=lambda row: row[0])
        output = main.RESULTS_DIR / "search" / name
        output.mkdir(parents=True, exist_ok=True)
        with (output / "ranking.txt").open("w", encoding="utf-8") as file:
            for rank, (_, method, params, count, quality, _) in enumerate(rows[:20], 1):
                file.write(f"{rank}: {method} params={params} count={count} quality={quality:.3f}\n")
        for rank, (_, method, params, count, _, detections) in enumerate(rows[:20], 1):
            image_out = main.draw_detections(image, detections)
            cv2.imwrite(str(output / f"{rank}_{method}_{count}.png"), image_out)


if __name__ == "__main__":
    main_search()
