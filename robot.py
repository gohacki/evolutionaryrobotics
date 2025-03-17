import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK


class ROBOT:
    def __init__(self):
        self.motors = {}
        self.sensors = {}
        self.robotID = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotID)
        self.nn = NEURAL_NETWORK("brain.nndf")
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
                # self.nn.Print()
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName).encode("utf-8")
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                if jointName in self.motors:
                    self.motors[jointName].Set_Value(self, desiredAngle)
                # print(neuronName, jointName, desiredAngle)


    def Think(self):
        self.nn.Update()


        
    def Save_Values(self):
        for sensor in self.sensors.values():
            sensor.Save_Values()
        for motor in self.motors.values():
            motor.Save_Values()

    def Get_Fitness(self):  # NEW:
        # Query the state of link zero using pybullet's getLinkState.
        stateOfLinkZero = p.getLinkState(self.robotID, 0)  # NEW:
        print("State of Link 0:", stateOfLinkZero)  # NEW:
        # exit()  # NEW: Uncomment for step verification if desired.
        
        # Extract the position tuple (the first element) from the state.
        positionOfLinkZero = stateOfLinkZero[0]  # NEW:
        print("Position of Link 0:", positionOfLinkZero)  # NEW:
        # exit()  # NEW: Uncomment for step verification if desired.
        
        # Extract the x-coordinate from the position tuple.
        xCoordinateOfLinkZero = positionOfLinkZero[0]  # NEW:
        print("X-coordinate of Link 0:", xCoordinateOfLinkZero)  # NEW:
        # exit()  # NEW: Uncomment for step verification if desired.
        
        # Write the x-coordinate (as a string) to fitness.txt.
        with open("fitness.txt", "w") as f:  # NEW:
            f.write(str(xCoordinateOfLinkZero))  # NEW:
        
