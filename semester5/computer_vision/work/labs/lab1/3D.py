import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.animation import FuncAnimation


# Вершини піраміди з квадратною основою
# Піраміда центрована відносно осі Z, тому вісь Z проходить
# через внутрішню область фігури
def create_pyramid(side=160, height=220):

    half = side / 2

    return np.array([
        [-half,  half,  half, -half, 0],
        [-half, -half,  half,  half, 0],
        [0,      0,    0,    0,    height],
        [1,      1,    1,    1,    1]
    ], dtype=float)


# Індекси вершин граней:
# A=0, B=1, C=2, D=3, S=4
FACES = [
    [0, 1, 2, 3],   # основа
    [0, 1, 4],      # передня грань
    [1, 2, 4],      # права грань
    [2, 3, 4],      # задня грань
    [3, 0, 4]       # ліва грань
]


def translation_matrix(dx, dy, dz):

    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ], dtype=float)


def rotation_x(angle_degrees):

    angle = np.deg2rad(angle_degrees)
    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def rotation_y(angle_degrees):

    angle = np.deg2rad(angle_degrees)
    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def rotation_z(angle_degrees):

    angle = np.deg2rad(angle_degrees)
    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def rotate_around_internal_axis(points, angle_degrees):

    move_axis_to_origin = translation_matrix(0, 0, 0)
    rotate = rotation_z(angle_degrees)
    move_axis_back = translation_matrix(0, 0, 0)

    transformation = (
        move_axis_back
        @ rotate
        @ move_axis_to_origin
    )

    return transformation @ points


def project_axonometric(points):

    view_rotation = rotation_y(-35) @ rotation_x(25)
    viewed_points = view_rotation @ points

    return viewed_points


def project_to_screen(points, width=800, height=650, scale=1.35):

    x = points[0, :] * scale + width / 2
    y = points[1, :] * scale + height / 2

    return np.vstack((x, y))


def transform_pyramid(pyramid, frame):

    angle = frame * 3

    rotated = rotate_around_internal_axis(
        pyramid,
        angle
    )

    return project_axonometric(rotated)


def create_face_patches(ax):

    patches = []

    for _ in FACES:
        patch = Polygon(
            [[0, 0], [0, 0], [0, 0]],
            closed=True,
            linewidth=2
        )
        ax.add_patch(patch)
        patches.append(patch)

    return patches


def update_face_patches(patches, points_2d, points_3d, frame, total_frames):

    # Плавна поява та зникнення
    visibility = 0.95 * (0.5 + 0.5 * np.sin(2 * np.pi * frame / total_frames))

    # Колір змінюється протягом анімації
    color_position = (frame % total_frames) / total_frames
    edge_color = plt.cm.hsv(color_position)

    for index, (patch, face) in enumerate(zip(patches, FACES)):
        face_points_2d = points_2d[:, face].T
        patch.set_xy(face_points_2d)

        # Різні грані мають різні відтінки заливки
        face_color = plt.cm.viridis((index / len(FACES) + color_position) % 1.0)

        patch.set_facecolor(face_color)
        patch.set_edgecolor(edge_color)
        patch.set_alpha(visibility)

        # Проста зміна порядку відображення граней за глибиною
        average_depth = np.mean(points_3d[2, face])
        patch.set_zorder(-average_depth)


def main():

    width = 800
    height = 650
    total_frames = 240

    fig, ax = plt.subplots(figsize=(9, 7))

    ax.set_title("3D піраміда: аксонометрична проекція та обертання")

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect("equal")
    ax.grid(True)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    pyramid = create_pyramid()

    patches = create_face_patches(ax)

    def init_animation():
        points_3d = transform_pyramid(pyramid, 0)
        points_2d = project_to_screen(
            points_3d,
            width,
            height
        )

        update_face_patches(
            patches,
            points_2d,
            points_3d,
            0,
            total_frames
        )

        return tuple(patches)

    def update_animation(frame):
        points_3d = transform_pyramid(pyramid, frame)
        points_2d = project_to_screen(
            points_3d,
            width,
            height
        )

        update_face_patches(
            patches,
            points_2d,
            points_3d,
            frame,
            total_frames
        )

        return tuple(patches)

    animation = FuncAnimation(
        fig,
        update_animation,
        init_func=init_animation,
        frames=total_frames,
        interval=40,
        repeat=True,
        blit=False
    )

    # Зберігаємо посилання animation до завершення роботи вікна
    _ = animation

    plt.show()

if __name__ == "__main__":
    main()
