# robot.py
import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os

class ROBOT:
    def __init__(self, solutionID):  # NEW: Accept solutionID
        self.solutionID = solutionID  # NEW:
        self.motors = {}
        self.sensors = {}
        self.robotID = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotID)
        # Use unique brain file name based on solutionID
        brainFile = "brain" + str(solutionID) + ".nndf"  # NEW:
        self.nn = NEURAL_NETWORK(brainFile)
        # Delete the brain file after it is read
        os.system("rm " + brainFile)  # NEW:
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
    
    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
    
    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, i):
        for sensor in self.sensors.values():
            sensor.Get_Value(i)

    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName).encode("utf-8")
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                if jointName in self.motors:
                    self.motors[jointName].Set_Value(self, desiredAngle)

    def Think(self):
        self.nn.Update()

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotID, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        # Write fitness into a temporary file then move it to a unique fitness file.
        tmpFile = "tmp" + str(self.solutionID) + ".txt"  # NEW:
        fitnessFile = "fitness" + str(self.solutionID) + ".txt"  # NEW:
        with open(tmpFile, "w") as f:
            f.write(str(xCoordinateOfLinkZero))
        os.system("mv " + tmpFile + " " + fitnessFile)  # NEW:
        return xCoordinateOfLinkZero
