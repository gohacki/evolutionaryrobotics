# simulation.py
import pybullet as p
import pybullet_data
import constants as c
from robot import ROBOT
from world import WORLD
import time

class SIMULATION:
    def __init__(self, directOrGUI, solutionID):  # NEW:
        self.directOrGUI = directOrGUI.upper()
        self.solutionID = solutionID  # NEW:
        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.setGravity(0, 0, c.GRAVITY)
        self.robot = ROBOT(solutionID)  # NEW: Pass solutionID to ROBOT
        self.world = WORLD()

    def Run(self):
        for i in range(c.ITERATIONS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            if self.directOrGUI == "GUI":
                time.sleep(c.SLEEPTIME)

    def Get_Fitness(self):
        return self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()
