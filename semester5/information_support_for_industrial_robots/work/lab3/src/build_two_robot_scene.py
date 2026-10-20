from pathlib import Path
import sys

sys.path.insert(0, '/opt/coppeliasim/programming/zmqRemoteApi/clients/python/src')
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

root = Path(__file__).parent
lua = (root / 'cw3_v317_two_robot_sorting.lua').read_text()
scene_path = str(root / 'cw3_v317_Davydchuk_IB_two_robot_sorting.ttt')

client = RemoteAPIClient('localhost', 23003)
sim = client.require('sim')
sim.loadScene('/opt/coppeliasim/system/dfltscn.ttt')

def shape(kind, size, pos, alias, color):
    h = sim.createPrimitiveShape(kind, size, 0)
    sim.setObjectAlias(h, alias)
    sim.setObjectPosition(h, sim.handle_world, pos)
    sim.setShapeColor(h, '', sim.colorcomponent_ambient_diffuse, color)
    return h

floor = shape(sim.primitiveshape_cuboid, [2.0, 1.6, 0.04], [0, 0.45, -0.02], 'WorkFloor', [0.48,0.48,0.52])
conveyor = shape(sim.primitiveshape_cuboid, [0.72, 0.30, 0.08], [-0.48, 0.82, 0.04], 'Conveyor', [0.12,0.15,0.18])
table = shape(sim.primitiveshape_cuboid, [0.82, 0.72, 0.08], [0.02, 0.55, 0.04], 'SortingTable', [0.55,0.58,0.62])

for i, x in enumerate([-0.78, -0.18]):
    shape(sim.primitiveshape_cylinder, [0.07, 0.07, 0.30], [x, 0.82, 0.10], 'ConveyorRoller' + str(i+1), [0.28,0.30,0.34])

for name, x, c in [('RedBin',0.22,[0.35,0.35,0.38]), ('GreenBin',0.45,[0.35,0.35,0.38]), ('BlueBin',0.68,[0.35,0.35,0.38])]:
    shape(sim.primitiveshape_cylinder, [0.16, 0.16, 0.16], [x, 0.22, 0.08], name, c)

r1 = sim.loadModel('/opt/coppeliasim/models/robots/non-mobile/ABB IRB 140.ttm')
sim.setObjectAlias(r1, 'Picker1')
sim.setObjectPosition(r1, sim.handle_world, [-0.72, 0.55, 0.0])
sim.setObjectOrientation(r1, sim.handle_world, [0,0,0])
r2 = sim.loadModel('/opt/coppeliasim/models/robots/non-mobile/ABB IRB 140.ttm')
sim.setObjectAlias(r2, 'Picker2')
sim.setObjectPosition(r2, sim.handle_world, [0.72, 0.55, 0.0])
sim.setObjectOrientation(r2, sim.handle_world, [0,0,3.141592653589793])

sensor = sim.createVisionSensor(1, [128,128,0,0], [0.01,3.0,1.0,1.0,0,0,0.02,0.02,0.02,0,0])
sim.setObjectAlias(sensor, 'ColorVisionSensor')
sim.setObjectPosition(sensor, sim.handle_world, [0.0, 0.55, 1.80])
sim.setObjectOrientation(sensor, sim.handle_world, [3.141592653589793, 0, 0])

script = sim.createScript(sim.scripttype_simulation, lua, 0, 'lua')
sim.setObjectAlias(script, 'TwoRobotSortingController')
sim.setObjectParent(script, r1, True)
sim.saveScene(scene_path)
print('scene saved:', scene_path)
print('handles:', sim.getObject('/Picker1/target'), sim.getObject('/Picker2/target'), sim.getObject('/ColorVisionSensor'))
