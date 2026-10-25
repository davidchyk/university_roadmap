import sys

sys.path.insert(0, '/opt/coppeliasim/programming/zmqRemoteApi/clients/python/src')
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

PORT = 23000
ROBOT = 'PioneerP3DX'
FORWARD_SPEED = 2.0
SAFE_DISTANCE = 0.4
SIMULATION_STEPS = 1_200
REVERSE_TIME = 0.7
TURN_TIME = 0.80

SENSORS_ON_LEFT = (1, 2, 3)
SENSORS_ON_RIGHT = (4, 5, 6)


def group_distance(sim, sensors, group):
    distances = []

    for sensor, sensor_index in sensors:
        if sensor_index in group:
            detected, distance, *_ = sim.readProximitySensor(sensor)

            if detected:
                distances.append(distance)

    return min(distances) if distances else float('inf')


def turning(sim, robot):
    left_distance = group_distance(sim, robot['front_sensors'], SENSORS_ON_LEFT)

    right_distance = group_distance(sim, robot['front_sensors'], SENSORS_ON_RIGHT)

    if left_distance < SAFE_DISTANCE and right_distance < SAFE_DISTANCE:

        return 'BACK_LEFT' if left_distance > right_distance else 'BACK_RIGHT'

    if left_distance < SAFE_DISTANCE:

        return 'RIGHT'

    if right_distance < SAFE_DISTANCE:
        return 'LEFT'

    return 'NONE'

def proc(sim, robot):
    now = sim.getSimulationTime()

    if robot['state'] == 'REVERSE':
        status = 'REVERSE'
        left_speed = right_speed = -1.5

        if now >= robot['state_until']:
            direction = robot['turn_after_reverse']
            robot['state'] = f'TURN_{direction}'
            robot['state_until'] = now + TURN_TIME

    elif robot['state'] == 'TURN_LEFT':
        status = 'TURN LEFT'
        left_speed, right_speed = -2.0, 2.5

        if now >= robot['state_until']:
            robot['state'] = 'TRACK'

    elif robot['state'] == 'TURN_RIGHT':
        status = 'TURN RIGHT'
        left_speed, right_speed = 2.5, -2.0

        if now >= robot['state_until']:
            robot['state'] = 'TRACK'

    else:
        action = turning(sim, robot)

        if action in ('BACK_LEFT', 'BACK_RIGHT'):
            direction = action.removeprefix('BACK_')
            robot['state'] = 'REVERSE'
            robot['state_until'] = now + REVERSE_TIME
            robot['turn_after_reverse'] = direction
            status = 'REVERSE'
            left_speed = right_speed = -1.5

        elif action == 'LEFT':
            status = 'AVOID LEFT'
            left_speed, right_speed = -2.0, 2.5

        elif action == 'RIGHT':
            status = 'AVOID RIGHT'
            left_speed, right_speed = 2.5, -2.0

        else:
            status = 'TRACK'
            left_speed = right_speed = FORWARD_SPEED

    sim.setJointTargetVelocity(robot['left_motor'], left_speed)
    sim.setJointTargetVelocity(robot['right_motor'], right_speed)

    if status != robot['last_status']:
        sim.addLog(
            sim.verbosity_scriptinfos,
            f"[{robot['name']}] {status}"
        )
        robot['last_status'] = status

def main():

    client = RemoteAPIClient('localhost', PORT)
    sim = client.require('sim')

    robots = []

    for index in range(5):
        name = f'/{ROBOT}[{index}]'

        robots.append({
            'name': name,
            'left_motor': sim.getObject(f'{name}/leftMotor'),
            'right_motor': sim.getObject(f'{name}/rightMotor'),
            'front_sensors': [
                (sim.getObject(f'{name}/ultrasonicSensor[{sensor_index}]'), sensor_index)
                for sensor_index in (1, 2, 3, 4, 5, 6)
            ],
            'state': 'TRACK',
            'state_until': 0.0,
            'turn_after_reverse': 'RIGHT',
            'last_status': None,
        })

    client.setStepping(True)
    sim.startSimulation()

    try:

        for _ in range(SIMULATION_STEPS):

            for robot in robots: proc(sim, robot)

            client.step()

    finally:

        for robot in robots:
            sim.setJointTargetVelocity(robot['left_motor'], 0.0)
            sim.setJointTargetVelocity(robot['right_motor'], 0.0)

        sim.stopSimulation()

if __name__ == '__main__':
    main()
