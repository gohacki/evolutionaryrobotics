import sys  # NEW: Import sys to access command line arguments
from simulation import SIMULATION

# NEW: Get the mode from the command line (DIRECT or GUI); default to DIRECT if not provided
if len(sys.argv) > 1:
    directOrGUI = sys.argv[1]
else:
    directOrGUI = "DIRECT"  # NEW:

simulation = SIMULATION(directOrGUI)  # NEW: Pass mode to the simulation constructor
simulation.Run()
simulation.Get_Fitness()
