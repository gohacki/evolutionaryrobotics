import pybullet as p
import pybullet_data
import constants as c
from robot import ROBOT
from world import WORLD
import time

class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.setGravity(0,0,c.GRAVITY)
        self.robot = ROBOT()
        self.world = WORLD()

    def Run(self):
        for i in range(c.ITERATIONS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Act(i)
            time.sleep(c.SLEEPTIME)
    def __del__(self):
        p.disconnect()

