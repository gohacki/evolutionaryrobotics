import numpy as np  # NEW:
import os           # NEW:
import pyrosim.pyrosim as pyrosim  # NEW:
import random       # NEW:

class SOLUTION:
    def __init__(self):
        # Create a 3x2 matrix of random values in the range [0,1] then scale to [-1,+1]
        self.weights = np.random.rand(3, 2)  # NEW:
        self.weights = self.weights * 2 - 1   # NEW:

    def Evaluate(self, mode):  # NEW: Added mode argument ("DIRECT" or "GUI")
        self.Create_World()   # NEW:
        self.Create_Body()    # NEW:
        self.Create_Brain()   # NEW:
        # NEW: Pass the mode argument to simulate.py on the command line.
        os.system("python simulate.py " + mode)  # NEW:
        with open("fitness.txt", "r") as fitnessFile:  # NEW:
            fitnessStr = fitnessFile.read().strip()     # NEW:
        self.fitness = float(fitnessStr)                # NEW:

    def Create_World(self):  # NEW:
        length, width, height = 1, 1, 1  # NEW:
        x, y, z = -3, 3, 0.5  # NEW:
        pyrosim.Start_SDF("world.sdf")  # NEW:
        pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])  # NEW:
        pyrosim.End()  # NEW:

    def Create_Body(self):  # NEW:
        length, width, height = 1, 1, 1  # NEW:
        pyrosim.Start_URDF("body.urdf")  # NEW:
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[length, width, height])  # NEW:
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[length, width, height])  # NEW:
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[length, width, height])  # NEW:
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[-0.5, 0, 1])  # NEW:
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0.5, 0, 1])  # NEW:
        pyrosim.End()  # NEW:

    def Create_Brain(self):  # NEW:
        pyrosim.Start_NeuralNetwork("brain.nndf")  # NEW:
        # Sensor neurons
        pyrosim.Send_Sensor_Neuron(name="0", linkName="Torso")  # NEW:
        pyrosim.Send_Sensor_Neuron(name="1", linkName="BackLeg")  # NEW:
        pyrosim.Send_Sensor_Neuron(name="2", linkName="FrontLeg")  # NEW:
        # Motor neurons (names start at 3)
        pyrosim.Send_Motor_Neuron(name="3", jointName="Torso_BackLeg")  # NEW:
        pyrosim.Send_Motor_Neuron(name="4", jointName="Torso_FrontLeg")  # NEW:
        # Create synapses using the current weight matrix
        for currentRow in range(3):  # NEW:
            for currentColumn in range(2):  # NEW:
                weight = self.weights[currentRow][currentColumn]  # NEW:
                # Source neuron is sensor currentRow; target neuron is motor (currentColumn + 3)
                pyrosim.Send_Synapse(sourceNeuronName=str(currentRow), targetNeuronName=str(currentColumn + 3), weight=weight)  # NEW:
        pyrosim.End()  # NEW:

    def Mutate(self):  # NEW:
        randomRow = random.randint(0, 2)  # NEW:
        randomColumn = random.randint(0, 1)  # NEW:
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1  # NEW:
