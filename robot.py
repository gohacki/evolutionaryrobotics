# robot.py
import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
import numpy as np

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
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                if jointName in self.motors:
                    self.motors[jointName].Set_Value(self, desiredAngle)

    def Think(self):
        self.nn.Update()

    def Get_Fitness(self, boxID):
        if self.robotID is None:
             fitness = 9999.0
        else:
             try:
                # Get the robot's position
                basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotID)
                basePosition = np.array(basePositionAndOrientation[0])

                # Get the box's position
                boxPositionAndOrientation = p.getBasePositionAndOrientation(boxID)
                boxPosition = np.array(boxPositionAndOrientation[0])

                # Compute Euclidean distance
                distance = np.linalg.norm(basePosition[0:2] - boxPosition[0:2])
                fitness = -distance

             except p.error as e:
                 print(f"PyBullet error getting positions for fitness calculation (Sol: {self.solutionID}): {e}")
                 fitness = 9999.0 # Assign high fitness on error


        # Write the fitness (i.e. distance) into a temporary file then move it
        tmpFile = "tmp" + str(self.solutionID) + ".txt"
        fitnessFile = "fitness" + str(self.solutionID) + ".txt"
        try:
            with open(tmpFile, "w") as f:
                f.write(str(fitness))
            # Use f-string for clarity and ensure command works on different OS if needed
            # Note: 'mv' is Linux/macOS, 'move' is Windows. Sticking with 'mv' based on your env.
            os.system(f"mv {tmpFile} {fitnessFile}")
        except Exception as e:
            print(f"Error writing or moving fitness file for solution {self.solutionID}: {e}")
            # If writing fails, the Wait_For_Simulation_To_End might hang or fail.
