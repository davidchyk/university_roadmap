from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
RESULTS_DIR = PROJECT_ROOT / "results"

# Параметри експерименту. Ratio test 0.65 залишає достатню кількість
# відповідностей і водночас відсіює неоднозначні пари дескрипторів.
RATIO_TEST = 0.65
RANSAC_REPROJECTION_THRESHOLD = 4.0
MIN_USABLE_MATCHES = 30
TARGET_PROBABILITY = 0.90
MAX_DRAW_MATCHES = 160
MAX_DRAW_KEYPOINTS = 1200


@dataclass(frozen=True)
class ComparisonResult:
    method: str
    keypoints_reference: int
    keypoints_candidate: int
    usable_matches: int
    inliers: int
    probability: float
    homography: np.ndarray
    reference_keypoints: list[cv2.KeyPoint]
    candidate_keypoints: list[cv2.KeyPoint]
    good_matches: list[cv2.DMatch]
    inlier_mask: np.ndarray


def load_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити зображення: {path}")
    return image


def preprocess(image: np.ndarray) -> np.ndarray:
    """Grayscale + локальне вирівнювання контрасту."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray)


def create_detector(method: str):
    if method == "ORB":
        return cv2.ORB_create(nfeatures=8000, fastThreshold=8), cv2.NORM_HAMMING
    if method == "SIFT" and hasattr(cv2, "SIFT_create"):
        return cv2.SIFT_create(nfeatures=8000, contrastThreshold=0.02), cv2.NORM_L2
    raise ValueError(f"Метод {method} недоступний у встановленій версії OpenCV")


def compare_images(
    reference_gray: np.ndarray,
    candidate_gray: np.ndarray,
    method: str,
) -> ComparisonResult:
    detector, norm = create_detector(method)
    reference_keypoints, reference_descriptors = detector.detectAndCompute(
        reference_gray, None
    )
    candidate_keypoints, candidate_descriptors = detector.detectAndCompute(
        candidate_gray, None
    )
    if reference_descriptors is None or candidate_descriptors is None:
        raise RuntimeError(f"{method}: не вдалося обчислити дескриптори")

    matcher = cv2.BFMatcher(norm)
    pairs = matcher.knnMatch(reference_descriptors, candidate_descriptors, k=2)
    good_matches = [
        first
        for pair in pairs
        if len(pair) == 2
        for first, second in [pair]
        if first.distance < RATIO_TEST * second.distance
    ]
    if len(good_matches) < MIN_USABLE_MATCHES:
        raise RuntimeError(
            f"{method}: лише {len(good_matches)} придатних відповідностей; "
            f"потрібно не менше {MIN_USABLE_MATCHES}"
        )

    # H переводить координати Bing-зображення в систему координат Landsat.
    candidate_points = np.float32(
        [candidate_keypoints[match.trainIdx].pt for match in good_matches]
    ).reshape(-1, 1, 2)
    reference_points = np.float32(
        [reference_keypoints[match.queryIdx].pt for match in good_matches]
    ).reshape(-1, 1, 2)
    homography, inlier_mask = cv2.findHomography(
        candidate_points,
        reference_points,
        cv2.RANSAC,
        RANSAC_REPROJECTION_THRESHOLD,
    )
    if homography is None or inlier_mask is None:
        raise RuntimeError(f"{method}: RANSAC не зміг оцінити гомографію")

    inlier_mask = inlier_mask.ravel().astype(bool)
    inliers = int(inlier_mask.sum())
    probability = inliers / len(good_matches)
    return ComparisonResult(
        method=method,
        keypoints_reference=len(reference_keypoints),
        keypoints_candidate=len(candidate_keypoints),
        usable_matches=len(good_matches),
        inliers=inliers,
        probability=probability,
        homography=homography,
        reference_keypoints=reference_keypoints,
        candidate_keypoints=candidate_keypoints,
        good_matches=good_matches,
        inlier_mask=inlier_mask,
    )


def draw_keypoints(image: np.ndarray, keypoints: list[cv2.KeyPoint]) -> np.ndarray:
    strongest = sorted(keypoints, key=lambda point: point.response, reverse=True)[
        :MAX_DRAW_KEYPOINTS
    ]
    return cv2.drawKeypoints(
        image,
        strongest,
        None,
        color=(0, 220, 255),
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
    )


def draw_inlier_matches(
    reference: np.ndarray,
    candidate: np.ndarray,
    result: ComparisonResult,
) -> np.ndarray:
    inlier_matches = [
        match
        for match, is_inlier in zip(result.good_matches, result.inlier_mask)
        if is_inlier
    ][:MAX_DRAW_MATCHES]
    return cv2.drawMatches(
        reference,
        result.reference_keypoints,
        candidate,
        result.candidate_keypoints,
        inlier_matches,
        None,
        matchColor=(0, 220, 0),
        singlePointColor=(0, 0, 255),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )


def draw_projected_region(
    reference: np.ndarray,
    candidate: np.ndarray,
    homography: np.ndarray,
) -> np.ndarray:
    result = reference.copy()
    height, width = candidate.shape[:2]
    corners = np.float32(
        [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]]
    ).reshape(-1, 1, 2)
    projected = cv2.perspectiveTransform(corners, homography)
    cv2.polylines(result, [np.int32(projected)], True, (0, 0, 255), 4, cv2.LINE_AA)
    return result


def save_method_results(
    method_dir: Path,
    reference: np.ndarray,
    candidate: np.ndarray,
    reference_gray: np.ndarray,
    candidate_gray: np.ndarray,
    result: ComparisonResult,
) -> None:
    method_dir.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(method_dir / "reference_preprocessed.png"), reference_gray)
    cv2.imwrite(str(method_dir / "candidate_preprocessed.png"), candidate_gray)
    cv2.imwrite(
        str(method_dir / "reference_keypoints.png"),
        draw_keypoints(reference, result.reference_keypoints),
    )
    cv2.imwrite(
        str(method_dir / "candidate_keypoints.png"),
        draw_keypoints(candidate, result.candidate_keypoints),
    )
    cv2.imwrite(
        str(method_dir / "inlier_matches.png"),
        draw_inlier_matches(reference, candidate, result),
    )
    cv2.imwrite(
        str(method_dir / "projected_region.png"),
        draw_projected_region(reference, candidate, result.homography),
    )
    warped = cv2.warpPerspective(
        candidate,
        result.homography,
        (reference.shape[1], reference.shape[0]),
    )
    blend = cv2.addWeighted(reference, 0.55, warped, 0.45, 0)
    cv2.imwrite(str(method_dir / "warped_candidate.png"), warped)
    cv2.imwrite(str(method_dir / "alignment_blend.png"), blend)


def save_summary(results: list[ComparisonResult]) -> None:
    with (RESULTS_DIR / "summary.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "method",
                "keypoints_reference",
                "keypoints_candidate",
                "usable_matches",
                "ransac_inliers",
                "identification_probability",
                "target_met",
            ]
        )
        for result in results:
            writer.writerow(
                [
                    result.method,
                    result.keypoints_reference,
                    result.keypoints_candidate,
                    result.usable_matches,
                    result.inliers,
                    f"{result.probability:.4f}",
                    result.probability >= TARGET_PROBABILITY,
                ]
            )


def main() -> None:
    cv2.setRNGSeed(42)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    reference = load_image(ROOT / "landsat.png")
    candidate = load_image(ROOT / "bing.png")
    reference_gray = preprocess(reference)
    candidate_gray = preprocess(candidate)

    results: list[ComparisonResult] = []
    for method in ("ORB", "SIFT"):
        result = compare_images(reference_gray, candidate_gray, method)
        results.append(result)
        save_method_results(
            RESULTS_DIR / method.lower(),
            reference,
            candidate,
            reference_gray,
            candidate_gray,
            result,
        )
        print(
            f"{method}: {result.inliers}/{result.usable_matches} RANSAC inliers, "
            f"P={result.probability:.4f}, target={result.probability >= TARGET_PROBABILITY}"
        )

    save_summary(results)
    best = max(results, key=lambda item: (item.probability, item.inliers))
    print(f"Обрано метод {best.method}; P={best.probability:.4f}")


if __name__ == "__main__":
    main()
