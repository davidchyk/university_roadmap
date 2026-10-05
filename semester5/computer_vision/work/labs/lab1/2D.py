import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.animation import FuncAnimation


def create_square(x=250, y=250, size=100):
    
    return np.array([
        [x,        x + size, x + size, x],
        [y,        y,        y + size, y + size],
        [1,        1,        1,        1]
    ], dtype=float)


def translation_matrix(dx, dy):

    return np.array([
        [1, 0, dx],
        [0, 1, dy],
        [0, 0, 1]
    ], dtype=float)


def scaling_matrix(sx, sy):

    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ], dtype=float)


def translate(M, dx, dy):

    T = np.array([
        [1, 0, dx],
        [0, 1, dy],
        [0, 0, 1]
    ], dtype=float)

    return T @ M


def get_center(M):

    cx = np.mean(M[0, :])
    cy = np.mean(M[1, :])

    return cx, cy


def scale_around_center(M, sx, sy, cx, cy):

    move_to_origin = translation_matrix(-cx, -cy)
    scale_matrix = scaling_matrix(sx, sy)
    move_back = translation_matrix(cx, cy)

    transformation = (
        move_back
        @ scale_matrix
        @ move_to_origin
    )

    return transformation @ M


def transform_square(square, frame):

    dx1 = 50 * np.sin(frame / 15)
    dy1 = 25 * np.cos(frame / 15)

    square_after_first_translation = translate(square, dx1, dy1)

    cx, cy = get_center(square_after_first_translation)

    scale_factor = (1.0 + 0.25 * np.sin(frame / 20))

    square_after_scaling = scale_around_center(square_after_first_translation, scale_factor, scale_factor, cx, cy)

    dx2 = 20 * np.cos(frame / 30)
    dy2 = 100 * np.sin(frame / 30)

    result = translate(square_after_scaling, dx2, dy2)

    return result


def matrix_to_points(M):

    return M[:2, :].T


def main():

    fig, ax = plt.subplots(figsize=(8, 7))

    ax.set_title("2D перетворення: переміщення + масштабування - переміщення")

    ax.set_xlim(0, 700)
    ax.set_ylim(0, 600)
    ax.set_aspect("equal")
    ax.grid(True)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    square = create_square()

    # Початкові координати квадрата
    initial_points = matrix_to_points(square)

    # Поточний квадрат
    polygon = Polygon(
        initial_points,
        closed=True,
        edgecolor="blue",
        facecolor="lightblue",
        linewidth=2,
        alpha=0.9
    )

    ax.add_patch(polygon)

    # Лінія траєкторії
    trajectory_line, = ax.plot(
        [],
        [],
        color="gray",
        linewidth=1.5,
        linestyle="--",
        label="Траєкторія"
    )

    ax.legend()

    def init_animation():
        polygon.set_xy(initial_points)
        trajectory_line.set_data([], [])

        return polygon, trajectory_line

    def update_animation(frame):
        # Поточне положення квадрата
        current_square = transform_square(
            square,
            frame
        )

        current_points = matrix_to_points(
            current_square
        )

        polygon.set_xy(current_points)

        # Обчислення траєкторії центра
        center_x = []
        center_y = []

        for previous_frame in range(frame + 1):
            previous_square = transform_square(
                square,
                previous_frame
            )

            previous_cx, previous_cy = get_center(
                previous_square
            )

            center_x.append(previous_cx)
            center_y.append(previous_cy)

        trajectory_line.set_data(
            center_x,
            center_y
        )

        return polygon, trajectory_line

    animation = FuncAnimation(
        fig,
        update_animation,
        init_func=init_animation,
        frames=240,
        interval=40,
        repeat=True,
        blit=False
    )

    plt.show()