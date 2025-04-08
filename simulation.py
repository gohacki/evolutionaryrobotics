# simulation.py
import pybullet as p
import pybullet_data
import constants as c
from robot import ROBOT
from world import WORLD  # Ensure WORLD is imported
import time
import os # Import os for potential use (though deletion is in WORLD now)

class SIMULATION:
    # Modify constructor to accept worldID and solutionID
    def __init__(self, directOrGUI, worldID, solutionID):
        self.directOrGUI = directOrGUI.upper()
        self.worldID = worldID      # Store worldID
        self.solutionID = solutionID  # Store solutionID

        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            # Suggestion: Slightly slow down GUI for better viewing if needed
            # self.physicsClient = p.connect(p.GUI, options='--opengl2')
            self.physicsClient = p.connect(p.GUI)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.setGravity(0, 0, c.GRAVITY)

        # Create the world FIRST, passing the worldID
        # This ensures the correct world is loaded before the robot
        self.world = WORLD(self.worldID) # Pass worldID to WORLD constructor

        # Then create the robot
        self.robot = ROBOT(solutionID) # Pass solutionID to ROBOT

    def Run(self):
        for i in range(c.ITERATIONS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            if self.directOrGUI == "GUI":
                # Adjust sleep time if simulation runs too fast/slow in GUI
                time.sleep(c.SLEEPTIME)

    def Get_Fitness(self):
        # The Get_Fitness method in ROBOT already handles writing the unique fitness file
        return self.robot.Get_Fitness()

    def __del__(self):
        # Check if physics client exists before disconnecting
        if hasattr(self, 'physicsClient') and p.isConnected(self.physicsClient):
             p.disconnect(self.physicsClient)
        # print(f"Simulation object for Sol {self.solutionID} World {self.worldID} destroyed, PyBullet disconnected.") # Optional debug print