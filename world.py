# world.py
import pybullet as p
import os # Import os for file operations

class WORLD:
    # Modify constructor to accept worldID
    def __init__(self, worldID):
        self.planeID = p.loadURDF("plane.urdf")

        # Construct the world filename based on worldID
        worldFilename = f"world{worldID}.sdf"

        # Check if the file exists before loading
        if os.path.exists(worldFilename):
            print(f"Loading world file: {worldFilename}") # Debug print
            p.loadSDF(worldFilename)

            # Delete the world file AFTER loading it
            try:
                os.remove(worldFilename)
                print(f"Deleted world file: {worldFilename}") # Debug print
            except OSError as e:
                print(f"Error deleting file {worldFilename}: {e}")
        else:
            print(f"Error: World file {worldFilename} not found!")
            # Consider exiting or raising an error if the world file is critical
            # For now, we'll just print an error and continue (simulation might be empty)