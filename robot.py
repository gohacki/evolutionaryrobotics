# robot.py

import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c

class ROBOT:
    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.motors = {}
        self.sensors = {}
        self.robotID = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotID)

        brainFile = "brain" + str(solutionID) + ".nndf"

        # Optional: Add a check here for debugging, though the error will happen anyway
        if not os.path.exists(brainFile):
             print(f"WARNING in ROBOT init: {brainFile} not found before loading.")

        self.nn = NEURAL_NETWORK(brainFile)

        # --- REMOVE OR COMMENT OUT THIS LINE ---
        # os.system("rm " + brainFile)
        # ---------------------------------------

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
                # Ensure jointName is bytes if motors dict expects bytes keys
                # Or decode if motors dict expects string keys
                jointName_str = self.nn.Get_Motor_Neurons_Joint(neuronName)
                # Assuming self.motors uses string keys based on Prepare_To_Act
                if jointName_str in self.motors:
                     desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                     self.motors[jointName_str].Set_Value(self, desiredAngle)
                # Handle the case where the joint name might not be found (optional robustness)
                # else:
                #    print(f"Warning: Joint '{jointName_str}' from NN not found in motors.")


    def Think(self):
        self.nn.Update()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotID)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]

        # Ensure atomicity: Write to temp file, then rename. This prevents
        # the main script reading an incomplete file if the simulation is slow.
        tmpFile = f"tmp_{self.solutionID}_{os.getpid()}.txt" # Unique temp file name
        fitnessFile = f"fitness{self.solutionID}.txt"
        try:
            with open(tmpFile, "w") as f:
                f.write(str(xPosition))
            # Rename is atomic on most systems
            os.rename(tmpFile, fitnessFile)
        except Exception as e:
            print(f"Error writing/renaming fitness file: {e}")
            # Clean up temp file if rename failed
            if os.path.exists(tmpFile):
                 os.remove(tmpFile)
        return xPosition