# simulate.py
import sys  # Import sys
from simulation import SIMULATION
import os # Import os for file deletion (though deletion happens in simulation.py/world.py now)

# --- Argument Parsing ---
# Default values
mode = "DIRECT"
worldID = "A"  # Default to World A if not specified
solutionID = "0" # Default ID

# Check arguments provided
if len(sys.argv) >= 2:
    mode = sys.argv[1].upper() # GUI or DIRECT

if len(sys.argv) >= 3:
    worldID = sys.argv[2].upper() # A or B
    if worldID not in ['A', 'B']:
        print(f"Error: Invalid worldID '{worldID}'. Must be 'A' or 'B'.")
        sys.exit(1) # Exit if invalid world ID

if len(sys.argv) >= 4:
    solutionID = sys.argv[3] # e.g., "0", "1", etc.
# --- End Argument Parsing ---


# Pass all three arguments to the SIMULATION constructor
simulation = SIMULATION(mode, worldID, solutionID)
simulation.Run()
simulation.Get_Fitness()

# Deletion of world file will happen inside SIMULATION/WORLD after loading

print(f"Simulation complete for Solution {solutionID} in World {worldID}. Fitness calculated.") # Added confirmation print