import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import math
import random
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.setGravity(0,0,-9.8)
planeID = p.loadURDF("plane.urdf")
robotID = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotID)
backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)

amplitude, frequency, phaseOffset = numpy.pi/4, 30, 0
targetAngles = amplitude * numpy.sin(frequency * numpy.linspace(0, 2 * numpy.pi, 1000) + phaseOffset)

amplitude2, frequency2, phaseOffset2 = numpy.pi/4, 30, numpy.pi/2
targetAngles2 = amplitude2 * numpy.sin(frequency2 * numpy.linspace(0, 2 * numpy.pi, 1000) + phaseOffset2)

for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotID,
        jointName = b'Torso_BackLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = targetAngles[i],
        maxForce = 50)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotID,
        jointName = b'Torso_FrontLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = targetAngles2[i],
        maxForce = 50)
    time.sleep(1/60)
p.disconnect()
with open('data/backLegSensorValues.npy', 'wb') as f:
    numpy.save(f, backLegSensorValues)
with open('data/frontLegSensorValues.npy', 'wb') as f:
    numpy.save(f, frontLegSensorValues)