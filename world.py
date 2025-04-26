import pybullet as p

class WORLD:
    def __init__(self):
        self.planeID = p.loadURDF("plane.urdf")
        boxIDs = p.loadSDF("world.sdf")
        if boxIDs:
             self.boxID = boxIDs[0] # Store the ID
        else:
             print("Error: world.sdf did not load any objects.")
             self.boxID = None # Indicate an error