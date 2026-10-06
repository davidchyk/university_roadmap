from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT.parent / "results"

# Параметри фільтрації
BLUR_KERNEL_SIZE = (5, 5)

CANNY_LOW_THRESHOLD = 50
CANNY_HIGH_THRESHOLD = 150

# Параметри локальної (адаптивної) бінаризації
# Розмір вікна має бути непарним числом
ADAPTIVE_BLOCK_SIZE = 21
ADAPTIVE_C = 3

# Мінімальна кількість методів, які повинні погодитися щодо пікселя
# Значення 3 дає консервативніші, але надійніші кандидати
CONSENSUS_REQUIRED = 3

# Площа контуру задається як частка площі всього зображення
MIN_AREA_RATIO = 0.0003
MAX_AREA_RATIO = 0.04

MIN_ASPECT_RATIO = 0.20
MAX_ASPECT_RATIO = 5.0

MIN_EXTENT = 0.20

# Параметри маски дахів/нейтральних ділянок
COLOR_CLOSE_KERNEL_SIZE = (7, 7)
COLOR_OPEN_KERNEL_SIZE = (3, 3)
COLOR_MIN_AREA_RATIO = 0.0002
COLOR_MAX_AREA_RATIO = 0.02
COLOR_MIN_ASPECT_RATIO = 0.20
COLOR_MAX_ASPECT_RATIO = 4.0
COLOR_MIN_EXTENT = 0.30

# Фото мають різну якість і освітлення, тому пороги маски різні
PHOTO_COLOR_CONFIGS = {
    "photo1": {"max_chroma": 15, "min_value": 90},
    "photo2": {"max_chroma": 20, "min_value": 110},
}

# Параметри порівняння двох зображень однієї території
REGISTRATION_MAX_FEATURES = 3000
REGISTRATION_RATIO_TEST = 0.75
REGISTRATION_RANSAC_THRESHOLD = 5.0
REGISTERED_CLOSE_KERNEL_SIZE = (3, 3)
REGISTERED_MIN_AREA_RATIO = 0.0002
REGISTERED_MAX_AREA_RATIO = 0.03
REGISTERED_MIN_ASPECT_RATIO = 0.20
REGISTERED_MAX_ASPECT_RATIO = 5.0
REGISTERED_MIN_EXTENT = 0.25


def load_image(path: Path) -> np.ndarray:

    image = cv2.imread(str(path), cv2.IMREAD_COLOR)

    if image is None:
        raise FileNotFoundError(f"Не вдалося завантажити зображення: {path}")

    return image


def detect_by_canny(image: np.ndarray) -> tuple[np.ndarray, list[np.ndarray]]:

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, BLUR_KERNEL_SIZE, 0)
    edges = cv2.Canny(
        blurred,
        threshold1=CANNY_LOW_THRESHOLD,
        threshold2=CANNY_HIGH_THRESHOLD,
    )

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    return edges, contours


def detect_by_threshold(image: np.ndarray) -> tuple[np.ndarray, list[np.ndarray]]:

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, BLUR_KERNEL_SIZE, 0)
    _, binary = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    return binary, contours


def detect_by_adaptive_threshold(
    image: np.ndarray,
) -> tuple[np.ndarray, list[np.ndarray]]:

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, BLUR_KERNEL_SIZE, 0)

    binary = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        ADAPTIVE_BLOCK_SIZE,
        ADAPTIVE_C,
    )

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    return binary, contours


def detect_by_color_mask(
    image: np.ndarray,
    max_chroma: int,
    min_value: int,
) -> tuple[np.ndarray, list[np.ndarray]]:

    blue, green, red = cv2.split(image)
    blue = blue.astype(np.int16)
    green = green.astype(np.int16)
    red = red.astype(np.int16)

    neutral_pixels = (
        (np.abs(red - green) <= max_chroma)
        & (np.abs(green - blue) <= max_chroma)
        & (red >= min_value)
        & (green >= min_value)
        & (blue >= min_value)
    )
    mask = neutral_pixels.astype(np.uint8) * 255

    close_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        COLOR_CLOSE_KERNEL_SIZE,
    )
    open_kernel = np.ones(COLOR_OPEN_KERNEL_SIZE, dtype=np.uint8)

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, open_kernel)

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    return mask, contours


def detect_by_consensus(
    threshold_mask: np.ndarray,
    adaptive_mask: np.ndarray,
    color_mask: np.ndarray,
) -> tuple[np.ndarray, list[np.ndarray]]:

    votes = (
        (threshold_mask > 0).astype(np.uint8)
        + (adaptive_mask > 0).astype(np.uint8)
        + (color_mask > 0).astype(np.uint8)
    )

    consensus_mask = (
        (votes >= CONSENSUS_REQUIRED).astype(np.uint8) * 255
    )

    contours, _ = cv2.findContours(
        consensus_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    return consensus_mask, contours


def filter_contours(
    contours: list[np.ndarray],
    image_shape: tuple[int, ...],
    min_area_ratio: float = MIN_AREA_RATIO,
    max_area_ratio: float = MAX_AREA_RATIO,
    min_aspect_ratio: float = MIN_ASPECT_RATIO,
    max_aspect_ratio: float = MAX_ASPECT_RATIO,
    min_extent: float = MIN_EXTENT,
    reject_border: bool = False,
) -> list[np.ndarray]:

    height, width = image_shape[:2]
    image_area = height * width
    min_area = image_area * min_area_ratio
    max_area = image_area * max_area_ratio

    valid = []

    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, box_width, box_height = cv2.boundingRect(contour)

        if reject_border and (
            x <= 2
            or y <= 2
            or x + box_width >= width - 2
            or y + box_height >= height - 2
        ):
            continue

        if box_height == 0 or box_width == 0:
            continue

        aspect_ratio = box_width / box_height
        extent = area / (box_width * box_height)

        if (
            min_area <= area <= max_area
            and min_aspect_ratio <= aspect_ratio <= max_aspect_ratio
            and extent >= min_extent
        ):
            valid.append(contour)

    return valid


def contour_center(contour: np.ndarray) -> tuple[int, int] | None:

    moments = cv2.moments(contour)

    if moments["m00"] == 0:
        return None

    center_x = int(moments["m10"] / moments["m00"])
    center_y = int(moments["m01"] / moments["m00"])
    return center_x, center_y


def draw_results(
    image: np.ndarray,
    contours: list[np.ndarray],
    title: str,
    output_path: Path,
) -> None:

    result = image.copy()

    for index, contour in enumerate(contours, start=1):
        cv2.drawContours(result, [contour], -1, (0, 255, 255), 2)

        center = contour_center(contour)
        if center is not None:
            cv2.putText(
                result,
                str(index),
                center,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

    rgb_result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(14, 8))
    plt.imshow(rgb_result)
    plt.title(f"{title} — знайдено об'єктів: {len(contours)}")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close()


def estimate_homography(
    source: np.ndarray,
    target: np.ndarray,
) -> tuple[np.ndarray | None, int]:

    source_gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(nfeatures=REGISTRATION_MAX_FEATURES)
    source_keypoints, source_descriptors = orb.detectAndCompute(
        source_gray,
        None,
    )
    target_keypoints, target_descriptors = orb.detectAndCompute(
        target_gray,
        None,
    )

    if source_descriptors is None or target_descriptors is None:
        return None, 0

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = matcher.knnMatch(
        source_descriptors,
        target_descriptors,
        k=2,
    )

    good_matches = [
        first
        for first, second in matches
        if first.distance < REGISTRATION_RATIO_TEST * second.distance
    ]

    if len(good_matches) < 4:
        return None, len(good_matches)

    source_points = np.float32(
        [source_keypoints[match.queryIdx].pt for match in good_matches]
    )
    target_points = np.float32(
        [target_keypoints[match.trainIdx].pt for match in good_matches]
    )

    homography, inlier_mask = cv2.findHomography(
        source_points,
        target_points,
        cv2.RANSAC,
        REGISTRATION_RANSAC_THRESHOLD,
    )

    if homography is None or inlier_mask is None:
        return None, 0

    return homography, int(inlier_mask.sum())


def detect_registered_color_consensus(
    reference_image: np.ndarray,
    second_image: np.ndarray,
    reference_name: str,
    second_name: str,
) -> tuple[np.ndarray, list[np.ndarray], np.ndarray | None, int]:

    reference_mask, _ = detect_by_color_mask(
        reference_image,
        **PHOTO_COLOR_CONFIGS[reference_name],
    )
    second_mask, _ = detect_by_color_mask(
        second_image,
        **PHOTO_COLOR_CONFIGS[second_name],
    )

    homography, inliers = estimate_homography(
        second_image,
        reference_image,
    )

    if homography is None:
        return np.zeros(reference_mask.shape, dtype=np.uint8), [], None, inliers

    reference_height, reference_width = reference_image.shape[:2]
    warped_second_mask = cv2.warpPerspective(
        second_mask,
        homography,
        (reference_width, reference_height),
        flags=cv2.INTER_NEAREST,
    )
    valid_area = cv2.warpPerspective(
        np.full(second_mask.shape, 255, dtype=np.uint8),
        homography,
        (reference_width, reference_height),
        flags=cv2.INTER_NEAREST,
    )

    common_mask = cv2.bitwise_and(reference_mask, warped_second_mask)
    common_mask = cv2.bitwise_and(common_mask, valid_area)

    close_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        REGISTERED_CLOSE_KERNEL_SIZE,
    )
    common_mask = cv2.morphologyEx(
        common_mask,
        cv2.MORPH_CLOSE,
        close_kernel,
    )

    contours, _ = cv2.findContours(
        common_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    return common_mask, contours, homography, inliers


def process_registered_pair(
    reference_path: Path,
    second_path: Path,
) -> int:

    reference_image = load_image(reference_path)
    second_image = load_image(second_path)

    common_mask, contours, homography, inliers = detect_registered_color_consensus(
        reference_image,
        second_image,
        "photo1",
        "photo2",
    )

    output = OUTPUT_DIR / "registered_pair"
    output.mkdir(parents=True, exist_ok=True)

    if homography is not None:
        warped_second = cv2.warpPerspective(
            second_image,
            homography,
            (reference_image.shape[1], reference_image.shape[0]),
        )
        alignment = cv2.addWeighted(
            reference_image,
            0.5,
            warped_second,
            0.5,
            0,
        )
        cv2.imwrite(str(output / "alignment_blend.png"), alignment)

    valid_contours = filter_contours(
        contours,
        reference_image.shape,
        min_area_ratio=REGISTERED_MIN_AREA_RATIO,
        max_area_ratio=REGISTERED_MAX_AREA_RATIO,
        min_aspect_ratio=REGISTERED_MIN_ASPECT_RATIO,
        max_aspect_ratio=REGISTERED_MAX_ASPECT_RATIO,
        min_extent=REGISTERED_MIN_EXTENT,
        reject_border=True,
    )

    cv2.imwrite(str(output / "registered_color_consensus_mask.png"), common_mask)
    draw_results(
        reference_image,
        valid_contours,
        f"Registered color consensus — {len(valid_contours)} об'єктів",
        output / "registered_color_consensus_result.png",
    )

    print(f"registered pair: inliers = {inliers}, candidates = {len(valid_contours)}")
    return len(valid_contours)


def process_photo(photo_path: Path, photo_name: str) -> dict[str, int]:

    image = load_image(photo_path)
    photo_output = OUTPUT_DIR / photo_name
    photo_output.mkdir(parents=True, exist_ok=True)

    canny_image, canny_contours = detect_by_canny(image)
    valid_canny = filter_contours(canny_contours, image.shape)

    threshold_image, threshold_contours = detect_by_threshold(image)
    valid_threshold = filter_contours(threshold_contours, image.shape)

    adaptive_image, adaptive_contours = detect_by_adaptive_threshold(image)
    valid_adaptive = filter_contours(adaptive_contours, image.shape)

    color_config = PHOTO_COLOR_CONFIGS[photo_name]
    color_image, color_contours = detect_by_color_mask(
        image,
        max_chroma=color_config["max_chroma"],
        min_value=color_config["min_value"],
    )
    valid_color = filter_contours(
        color_contours,
        image.shape,
        min_area_ratio=COLOR_MIN_AREA_RATIO,
        max_area_ratio=COLOR_MAX_AREA_RATIO,
        min_aspect_ratio=COLOR_MIN_ASPECT_RATIO,
        max_aspect_ratio=COLOR_MAX_ASPECT_RATIO,
        min_extent=COLOR_MIN_EXTENT,
        reject_border=True,
    )

    consensus_image, consensus_contours = detect_by_consensus(
        threshold_image,
        adaptive_image,
        color_image,
    )
    valid_consensus = filter_contours(consensus_contours, image.shape)

    cv2.imwrite(str(photo_output / "canny_edges.png"), canny_image)
    cv2.imwrite(str(photo_output / "threshold.png"), threshold_image)
    cv2.imwrite(str(photo_output / "adaptive_threshold.png"), adaptive_image)
    cv2.imwrite(str(photo_output / "color_mask.png"), color_image)
    cv2.imwrite(str(photo_output / "consensus_mask.png"), consensus_image)

    draw_results(
        image,
        valid_canny,
        f"{photo_name}: Canny",
        photo_output / "canny_result.png",
    )
    draw_results(
        image,
        valid_threshold,
        f"{photo_name}: Threshold",
        photo_output / "threshold_result.png",
    )
    draw_results(
        image,
        valid_adaptive,
        f"{photo_name}: Adaptive threshold",
        photo_output / "adaptive_result.png",
    )
    draw_results(
        image,
        valid_color,
        f"{photo_name}: Color mask",
        photo_output / "color_result.png",
    )
    draw_results(
        image,
        valid_consensus,
        f"{photo_name}: Consensus",
        photo_output / "consensus_result.png",
    )

    return {
        "canny": len(valid_canny),
        "threshold": len(valid_threshold),
        "adaptive": len(valid_adaptive),
        "color": len(valid_color),
        "consensus": len(valid_consensus),
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = {
        "photo1": process_photo(ROOT / "photo1.png", "photo1"),
        "photo2": process_photo(ROOT / "photo2.png", "photo2"),
    }

    print("Результати обробки:")
    for photo_name, counts in results.items():
        print(
            f"{photo_name}: "
            f"Canny = {counts['canny']}, "
            f"Threshold = {counts['threshold']}, "
            f"Adaptive = {counts['adaptive']}, "
            f"Color mask = {counts['color']}, "
            f"Consensus = {counts['consensus']}"
        )

    process_registered_pair(
        ROOT / "photo1.png",
        ROOT / "photo2.png",
    )


if __name__ == "__main__":
    main()
