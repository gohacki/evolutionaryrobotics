import pybullet as p
import pybullet_data
import constants as c
from robot import ROBOT
from world import WORLD
import time

class SIMULATION:
    def __init__(self, directOrGUI):  # NEW:
        self.directOrGUI = directOrGUI.upper()  # NEW: Save mode for later use
        if self.directOrGUI == "DIRECT":  # NEW:
            self.physicsClient = p.connect(p.DIRECT)  # NEW:
        else:
            self.physicsClient = p.connect(p.GUI)  # NEW:
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.setGravity(0, 0, c.GRAVITY)
        self.robot = ROBOT()
        self.world = WORLD()

    def Run(self):
        for i in range(c.ITERATIONS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            # Only pause if running in GUI mode to allow you to watch the simulation.
            if self.directOrGUI == "GUI":  # NEW:
                time.sleep(c.SLEEPTIME)  # NEW:

    def Get_Fitness(self):
        return self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()
