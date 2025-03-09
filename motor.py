import constants as c
import numpy
import pyrosim.pyrosim as pyrosim
import pybullet as p


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName

    def Set_Value(self, robot, desiredAngle):
        targetPosition = desiredAngle
        pyrosim.Set_Motor_For_Joint(
            bodyIndex     = robot.robotID,
            jointName     = self.jointName,
            controlMode   = p.POSITION_CONTROL,
            targetPosition= targetPosition,
            maxForce      = c.MAXFORCE
        )