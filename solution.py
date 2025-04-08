# solution.py
import numpy as np
import os
import pyrosim.pyrosim as pyrosim
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        # Initialize weights randomly
        self.weights = (np.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2) - 1
        # Initialize fitness to a very large value (representing bad fitness)
        self.fitness = float('inf')

    def Set_ID(self, newID):
        self.myID = newID

    # --- NEW Evaluate Method ---
    # This method now handles the entire evaluation process for ONE solution
    # across BOTH worlds.
    def Evaluate(self, mode):
        # 1. Create necessary files ONCE per evaluation
        #    Generate_World creates both worldA.sdf and worldB.sdf
        self.Generate_World()
        self.Create_Body() # Only needs creation once if structure is fixed
        self.Create_Brain() # Create the brain file for this solution ID

        total_fitness = 0.0
        num_simulations = 0

        # 2. Run Simulation for World A
        print(f"-- Starting Simulation for Solution {self.myID} in World A --")
        self.Start_Single_Simulation(mode, 'A')
        fitnessA = self.Wait_For_Single_Simulation_To_End()
        print(f"-- Finished Simulation for Solution {self.myID} in World A (Fitness: {fitnessA:.4f}) --")
        if fitnessA is not None:
            total_fitness += fitnessA
            num_simulations += 1


        # 3. Run Simulation for World B
        print(f"-- Starting Simulation for Solution {self.myID} in World B --")
        self.Start_Single_Simulation(mode, 'B')
        fitnessB = self.Wait_For_Single_Simulation_To_End()
        print(f"-- Finished Simulation for Solution {self.myID} in World B (Fitness: {fitnessB:.4f}) --")
        if fitnessB is not None:
            total_fitness += fitnessB
            num_simulations += 1


        # 4. Calculate Average Fitness
        if num_simulations > 0:
             self.fitness = total_fitness / num_simulations
        else:
             self.fitness = float('inf') # Assign poor fitness if both sims failed

        print(f"Solution {self.myID} | World A Fit: {fitnessA:.4f} | World B Fit: {fitnessB:.4f} | Avg Fitness: {self.fitness:.4f}")
        print("-" * 30) # Separator

        # Note: worldA.sdf and worldB.sdf are deleted by simulation.py/world.py after loading


    # Renamed from Start_Simulation - starts only ONE simulation instance
    def Start_Single_Simulation(self, mode, worldID):
        # Command now needs mode, worldID, and solutionID
        # Use & to run in the background on Linux/macOS
        # Use start /B python ... on Windows if background execution is needed and works
        # The "2&>1" redirects stderr to stdout, useful for catching errors
        # The final "&" runs it in the background (Linux/macOS)
        # --- MODIFY THIS LINE ---
        # cmd = f"python simulate.py {mode} {worldID} {str(self.myID)} > /dev/null 2>&1 &"
        cmd = f"python simulate.py {mode} {worldID} {str(self.myID)} &" # REMOVE output redirection
        # ------------------------
        # On Windows, you might need:
        # cmd = f"start /B python simulate.py {mode} {worldID} {str(self.myID)}"
        print(f"Executing command: {cmd}") # Debug print
        os.system(cmd)

    # Renamed from Wait_For_Simulation_To_End - waits for ONE simulation instance
    # Reads the fitness file, returns the value, and DELETES the file.
    def Wait_For_Single_Simulation_To_End(self):
        fitnessFileName = f"fitness{self.myID}.txt"
        start_time = time.time()
        timeout_seconds = 60 # Wait max 60 seconds for a simulation

        while not os.path.exists(fitnessFileName):
            time.sleep(0.05) # Check less frequently
            if time.time() - start_time > timeout_seconds:
                 print(f"Timeout waiting for {fitnessFileName}")
                 return None # Indicate failure

        # Wait a tiny bit longer to ensure file writing is complete
        time.sleep(0.1)

        try:
            with open(fitnessFileName, "r") as fitnessFile:
                fitnessStr = fitnessFile.read().strip()
            current_fitness = float(fitnessStr)
            os.remove(fitnessFileName) # Delete the file immediately after reading
            # print(f"Read and deleted {fitnessFileName}, fitness: {current_fitness}") # Debug print
            return current_fitness
        except FileNotFoundError:
            print(f"Error: {fitnessFileName} disappeared before reading.")
            return None # Indicate failure
        except ValueError:
            print(f"Error: Could not convert fitness '{fitnessStr}' from {fitnessFileName} to float.")
            # Attempt to delete the corrupted file anyway
            if os.path.exists(fitnessFileName):
                os.remove(fitnessFileName)
            return None # Indicate failure
        except Exception as e:
            print(f"An unexpected error occurred reading {fitnessFileName}: {e}")
            if os.path.exists(fitnessFileName):
                os.remove(fitnessFileName)
            return None # Indicate failure


    # Renamed from Create_World to avoid confusion with world.py's class
    # This GENERATES the world files based on Milestone 1 logic
    def Generate_World(self):
        length, width, height = 1, 1, 1
        z = 0.5

        # Generate random positions for worldA
        xA = random.uniform(-5, 5)
        yA = random.uniform(-5, 5)

        # Create worldA.sdf
        pyrosim.Start_SDF("worldA.sdf")
        pyrosim.Send_Cube(name="Box", pos=[xA, yA, z], size=[length, width, height])
        pyrosim.End()

        # Generate random positions for worldB
        xB = random.uniform(-5, 5)
        yB = random.uniform(-5, 5)

        # Create worldB.sdf
        pyrosim.Start_SDF("worldB.sdf")
        pyrosim.Send_Cube(name="Box", pos=[xB, yB, z], size=[length, width, height])
        pyrosim.End()
        # print("Generated worldA.sdf and worldB.sdf") # Debug print


    def Create_Body(self):
        # (Keep your existing Create_Body logic here)
        # ... (your existing code) ...
        length, width, height = 1, 1, 1
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[length, width, height])
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2,1,0.2])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, .5, 0], size=[0.2,1,0.2])
        pyrosim.Send_Cube(name="LeftLeg", pos=[-.5, 0, 0], size=[1,0.2,0.2])
        pyrosim.Send_Cube(name="RightLeg", pos=[.5, 0, 0], size=[1,0.2,0.2])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0, -.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0, .5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[-.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[.5, 0, 1], jointAxis = "0 1 0")
        # --- Lower legs ---
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -.5], size=[0.2, .2, 1])
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg",parent="FrontLeg",child="FrontLowerLeg",type="revolute",position=[0, 1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg",parent="BackLeg",child="BackLowerLeg",type="revolute",position=[0, -1, 0],jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -.5], size=[.2, 0.2, 1])
        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg",parent="LeftLeg",child="LeftLowerLeg",type="revolute",position=[-1, 0, 0],jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position=[1, 0, 0], jointAxis="0 1 0")
        pyrosim.End()
        # print("Generated body.urdf") # Debug print

    def Create_Brain(self):
        brainFileName = f"brain{self.myID}.nndf" # Use unique filename
        pyrosim.Start_NeuralNetwork(brainFileName)
        # (Keep your existing Create_Brain logic here using self.weights)
        # ... (your existing code) ...
        # Sensor neurons for lower legs
        pyrosim.Send_Sensor_Neuron(name="0", linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name="1", linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name="2", linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name="3", linkName="RightLowerLeg")

        # Motor neurons (names start after sensor neurons)
        motor_neuron_start_index = c.numSensorNeurons
        pyrosim.Send_Motor_Neuron(name=str(motor_neuron_start_index + 0), jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=str(motor_neuron_start_index + 1), jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=str(motor_neuron_start_index + 2), jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=str(motor_neuron_start_index + 3), jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=str(motor_neuron_start_index + 4), jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=str(motor_neuron_start_index + 5), jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=str(motor_neuron_start_index + 6), jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=str(motor_neuron_start_index + 7), jointName="RightLeg_RightLowerLeg")

        # Synapses
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                weight = self.weights[currentRow][currentColumn]
                source_name = str(currentRow)
                target_name = str(currentColumn + c.numSensorNeurons) # Target names start after sensor names
                pyrosim.Send_Synapse(sourceNeuronName=source_name, targetNeuronName=target_name, weight=weight)

        pyrosim.End()
        # print(f"Generated {brainFileName}") # Debug print

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons-1)
        randomColumn = random.randint(0, c.numMotorNeurons-1)
        # Apply mutation with a Gaussian distribution centered at 0
        mutation_value = random.gauss(0, 1.0) # Mean 0, Stddev 1.0 - adjust stddev as needed
        self.weights[randomRow, randomColumn] += mutation_value
        # Optional: Clamp weights to [-1, 1] range if they grow too large
        self.weights[randomRow, randomColumn] = max(-1.0, min(1.0, self.weights[randomRow, randomColumn]))
        # print(f"Mutated weight at [{randomRow},{randomColumn}]") # Debug print