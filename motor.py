import constants as c
import numpy
import pyrosim.pyrosim as pyrosim
import pybullet as p


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.motorValues = numpy.zeros(c.ITERATIONS)

        self.amplitude = c.AMPLITUDE
        self.offset    = c.PHASEOFFSET

        if self.jointName == b'Torso_BackLeg':
            self.frequency = c.FREQUENCY / 2
        else:
            self.frequency = c.FREQUENCY

        self.motorValues = self.amplitude * numpy.sin(
            self.frequency * numpy.linspace(c.RANGESTART, c.RANGEEND, c.ITERATIONS) + self.offset
        )

    def Set_Value(self, robot, i):
        targetPosition = self.motorValues[i]
        pyrosim.Set_Motor_For_Joint(
            bodyIndex     = robot.robotID,
            jointName     = self.jointName,
            controlMode   = p.POSITION_CONTROL,
            targetPosition= targetPosition,
            maxForce      = c.MAXFORCE
        )
    
    def Save_Values(self):
        import numpy as np
        np.save('data/{}_MotorValues.npy'.format(self.jointName), self.motorValues)