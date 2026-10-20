from pathlib import Path
import math
import sys

sys.path.insert(0, '/opt/coppeliasim/programming/zmqRemoteApi/clients/python/src')
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path('/home/davydchuk/projects/ur')
SCENE = ROOT / 'semester5/information_support_for_industrial_robots/work/lab3/src/cw3_v317_Davydchuk_IB_two_robot_sorting.ttt'
FRAMES = ROOT / 'semester5/information_support_for_industrial_robots/work/lab3/docs/lab3_frames_side_50fps'
FRAMES.mkdir(parents=True, exist_ok=True)

MAX_SIMULATION_STEPS = 800
CAPTURE_FPS = 50
SENSOR_RESOLUTION = (1024, 576)
OUTPUT_RESOLUTION = (960, 540)


def normalize(vector):
    length = math.sqrt(sum(value * value for value in vector))
    return [value / length for value in vector]


def cross(left, right):
    return [
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    ]


def look_at_matrix(eye, target):
    """Camera matrix: local Z points at target, while local Y points upward."""
    forward = normalize([target[i] - eye[i] for i in range(3)])
    right = normalize(cross([0.0, 0.0, 1.0], forward))
    up = cross(forward, right)
    return [
        right[0], up[0], forward[0], eye[0],
        right[1], up[1], forward[1], eye[1],
        right[2], up[2], forward[2], eye[2],
    ]

client = RemoteAPIClient('localhost', 23017)
sim = client.require('sim')
sim.loadScene(str(SCENE))

# A separate perspective sensor is used only to capture the report image.
# The operational ColorVisionSensor stays above and continues detecting balls.
sensor = sim.createVisionSensor(
    1 + 2 + 4 + 64 + 128,
    [SENSOR_RESOLUTION[0], SENSOR_RESOLUTION[1], 0, 0],
    [
        0.02,
        5.0,
        math.radians(58.0),
        0.05,
        0.0,
        0.0,
        0.70,
        0.73,
        0.78,
        0.0,
        0.0,
    ],
)
sim.setObjectAlias(sensor, 'ReportCaptureSensor')
camera_position = [1.45, -1.10, 0.88]
camera_target = [0.0, 0.55, 0.20]
sim.setObjectMatrix(
    sensor,
    sim.handle_world,
    look_at_matrix(camera_position, camera_target),
)

client.setStepping(True)
sim.setFloatParam(sim.floatparam_simulation_time_step, 1.0 / CAPTURE_FPS)
sim.startSimulation()

saved = 0
pause_frames = 0
for step in range(MAX_SIMULATION_STEPS):
    client.step()
    sim.handleVisionSensor(sensor)
    raw, resolution = sim.getVisionSensorImg(sensor, 0)
    width, height = resolution
    image = Image.frombytes('RGB', (width, height), raw)
    image = ImageOps.flip(image)
    image = image.resize(OUTPUT_RESOLUTION, Image.Resampling.LANCZOS)
    image = ImageEnhance.Contrast(image).enhance(1.06)
    image = image.filter(ImageFilter.UnsharpMask(radius=0.7, percent=115, threshold=3))
    image.save(
        FRAMES / f'report-{saved:03d}.jpg',
        format='JPEG',
        quality=82,
        subsampling=0,
        optimize=True,
    )
    saved += 1

    phase = sim.getStringSignal('TwoRobotPhase')
    if phase == 'pause':
        pause_frames += 1
        if pause_frames >= 30:
            break

sim.stopSimulation()
print(f'Saved {saved} frames at {CAPTURE_FPS} FPS to {FRAMES}')
