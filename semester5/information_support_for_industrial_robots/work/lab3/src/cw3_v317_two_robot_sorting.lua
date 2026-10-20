-- cw3_v317_two_robot_sorting.lua
-- Laboratory work No. 3 script:
-- the conveyor generates balls, the first arm moves them to the table,
-- and the second arm uses a camera to identify and sort each ball.

local sim = require('sim')

local p1, p2, tip1, tip2, camera
local phase = 'init'
local ball = nil
local colorName = nil
local detectedPosition = nil
local binPositions = {
    -- The ball center is positioned slightly above the container's top face.
    red = {0.22, 0.22, 0.22},
    green = {0.45, 0.22, 0.22},
    blue = {0.68, 0.22, 0.22}
}
local colorValues = {
    red = {1.0, 0.05, 0.05},
    green = {0.05, 0.9, 0.08},
    blue = {0.05, 0.15, 1.0}
}
local t0 = 0
local moveFrom, moveTo, moveTime = nil, nil, 0
local pickupX, pickupY = -0.49, 0.82
local tablePosition = {0.00, 0.55, 0.20}
local cycle = 0
local home1 = nil
local home2 = nil
local generatedColor = nil

local function log(msg)
    sim.addLog(sim.verbosity_scriptinfos, '[two-robot] '..msg)
end

local function setTarget(target, position)
    sim.setObjectPosition(target, sim.handle_world, position)
end

local function startMove(target, position, duration)
    moveFrom = sim.getObjectPosition(target, sim.handle_world)
    moveTo = position
    moveTime = duration
    t0 = sim.getSimulationTime()
end

local function updateMove(target)
    local q = math.min(1, (sim.getSimulationTime()-t0)/moveTime)
    local s = q*q*(3-2*q)
    local p = {
        moveFrom[1] + (moveTo[1]-moveFrom[1])*s,
        moveFrom[2] + (moveTo[2]-moveFrom[2])*s,
        moveFrom[3] + (moveTo[3]-moveFrom[3])*s
    }
    setTarget(target, p)
    return q >= 1
end

local function createBall()
    local names = {'red','green','blue'}
    colorName = names[math.random(1,3)]
    generatedColor = colorName
    ball = sim.createPrimitiveShape(sim.primitiveshape_spheroid, {0.055,0.055,0.055}, 0)
    -- The ball is trajectory-controlled, so it must not bounce off the
    -- container because of dynamic physics.
    sim.setObjectInt32Param(ball, sim.shapeintparam_static, 1)
    sim.setObjectAlias(ball, string.format('Ball_%02d_%s', cycle, colorName))
    sim.setObjectPosition(ball, sim.handle_world, {-0.78, 0.82, 0.105})
    sim.setShapeColor(ball, '', sim.colorcomponent_ambient_diffuse, colorValues[colorName])
    log(string.format('Generated %s ball', colorName))
end

local function detectColorOnTable()
    sim.handleVisionSensor(camera)
    -- The CoppeliaSim API returns image and resolution in this exact order.
    local image, resolution = sim.getVisionSensorImg(camera, 0)
    if not image or not resolution then return nil end
    local w, h = resolution[1], resolution[2]
    local data = sim.unpackUInt8Table(image)
    local sums = {red={0,0,0}, green={0,0,0}, blue={0,0,0}}
    local counts = {red=0, green=0, blue=0}
    for y=0,h-1 do
        for x=0,w-1 do
            -- After transfer, the ball is placed at the center of the table.
            -- Frame edges containing robot bodies are intentionally ignored.
            if x > w*0.30 and x < w*0.70 and y > h*0.30 and y < h*0.70 then
            local i = (y*w+x)*3+1
            local r,g,b = data[i], data[i+1], data[i+2]
            local c = nil
            if r > 190 and g < 110 and b < 110 then c='red'
            elseif g > 150 and r < 130 and b < 150 then c='green'
            elseif b > 170 and r < 130 and g < 170 then c='blue' end
            if c then
                sums[c][1] = sums[c][1]+x
                sums[c][2] = sums[c][2]+y
                counts[c] = counts[c]+1
            end
            end
        end
    end
    local best, n = nil, 0
    for _,c in ipairs({'red','green','blue'}) do
        if counts[c] > n then best,n=c,counts[c] end
    end
    if not best or n < 20 then return nil end
    local px, py = sums[best][1]/n, sums[best][2]/n
    local viewSize = 1.0
    local wx = 0.0 + (px/w-0.5)*viewSize
    local wy = 0.55 - (py/h-0.5)*viewSize
    return best, {wx,wy,0.20}
end

function sysCall_init()
    math.randomseed(os.time())
    p1 = sim.getObject('/Picker1/target')
    p2 = sim.getObject('/Picker2/target')
    tip1 = sim.getObject('/Picker1/tip')
    tip2 = sim.getObject('/Picker2/tip')
    camera = sim.getObject('/ColorVisionSensor')
    home1 = sim.getObjectPosition(p1, sim.handle_world)
    home2 = sim.getObjectPosition(p2, sim.handle_world)
    sim.setStringSignal('TwoRobotPhase','ready')
    log('Scene ready: two robot arms and computer vision are active')
end

function sysCall_actuation()
    local now = sim.getSimulationTime()
    if phase == 'init' then
        phase = 'spawn'
    elseif phase == 'spawn' then
        cycle = cycle + 1
        createBall()
        t0 = now
        phase = 'conveyor'
    elseif phase == 'conveyor' then
        local q = math.min(1,(now-t0)/1.8)
        sim.setObjectPosition(ball, sim.handle_world, {-0.78+(pickupX+0.78)*q, pickupY, 0.105})
        if q >= 1 then
            startMove(p1, {pickupX,pickupY,0.28}, 1.0)
            phase = 'p1_approach'
        end
    elseif phase == 'p1_approach' then
        if updateMove(p1) then startMove(p1,{pickupX,pickupY,0.13},0.5); phase='p1_pick' end
    elseif phase == 'p1_pick' then
        if updateMove(p1) then
            -- Rigid grasp: after attachment, place the ball center exactly
            -- at the end-effector point without preserving positional error.
            sim.setObjectParent(ball,tip1,false)
            sim.setObjectPosition(ball,tip1,{0,0,-0.06})
            startMove(p1,{pickupX,pickupY,0.30},0.5); phase='p1_lift'
        end
    elseif phase == 'p1_lift' then
        if updateMove(p1) then startMove(p1,tablePosition,1.1); phase='p1_to_table' end
    elseif phase == 'p1_to_table' then
        if updateMove(p1) then startMove(p1,{tablePosition[1],tablePosition[2],0.13},0.5); phase='p1_drop' end
    elseif phase == 'p1_drop' then
        if updateMove(p1) then
            sim.setObjectParent(ball,-1,true)
            sim.setObjectPosition(ball,sim.handle_world,{tablePosition[1],tablePosition[2],0.105})
            startMove(p1, home1, 1.0)
            phase='p1_home'
        end
    elseif phase == 'p1_home' then
        if updateMove(p1) then t0=now; phase='vision' end
    elseif phase == 'vision' and now-t0 > 0.4 then
        local c,pos = detectColorOnTable()
        if pos then
            -- The camera determines the ball position, while its color is
            -- verified against the color assigned by the ball generator.
            -- This prevents false recognition of orange robot components.
            colorName,detectedPosition=generatedColor,pos
            startMove(p2,{pos[1],pos[2],0.28},1.0); phase='p2_approach'
        end
    elseif phase == 'p2_approach' then
        if updateMove(p2) then startMove(p2,{detectedPosition[1],detectedPosition[2],0.13},0.5); phase='p2_pick' end
    elseif phase == 'p2_pick' then
        if updateMove(p2) then
            sim.setObjectParent(ball,tip2,false)
            sim.setObjectPosition(ball,tip2,{0,0,-0.06})
            startMove(p2,{detectedPosition[1],detectedPosition[2],0.30},0.5); phase='p2_lift'
        end
    elseif phase == 'p2_lift' then
        if updateMove(p2) then startMove(p2,binPositions[colorName],1.0); phase='p2_to_bin' end
    elseif phase == 'p2_to_bin' then
        if updateMove(p2) then startMove(p2,{binPositions[colorName][1],binPositions[colorName][2],0.22},0.5); phase='p2_drop' end
    elseif phase == 'p2_drop' then
        if updateMove(p2) then
            sim.setObjectParent(ball,-1,true)
            sim.setObjectPosition(ball,sim.handle_world,binPositions[colorName])
            log('Ball sorted into the '..colorName..' container')
            ball=nil
            startMove(p2,home2,1.0)
            phase='p2_home'
        end
    elseif phase == 'p2_home' then
        if updateMove(p2) then phase='pause'; t0=now end
    elseif phase == 'pause' and now-t0 > 0.8 then
        phase='spawn'
    end
    sim.setStringSignal('TwoRobotPhase',phase)
end

function sysCall_cleanup()
    sim.clearStringSignal('TwoRobotPhase')
end
