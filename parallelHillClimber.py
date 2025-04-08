# parallelHillClimber.py
import os
from solution import SOLUTION
from constants import populationSize, numberOfGenerations
import copy
import time # Import time for potential delays

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf 2> /dev/null") # Suppress errors if no files exist
        os.system("rm fitness*.txt 2> /dev/null")
        os.system("rm world*.sdf 2> /dev/null") # Clean up world files too
        self.nextAvailableID = 0
        self.parents = {}
        for i in range(populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID) # Use 'i' as the key directly
            self.nextAvailableID += 1
        print("Initialized Parallel Hill Climber with population size:", populationSize)

    def Evolve(self):
        # Evaluate initial parents
        print("\n--- Evaluating Initial Parents ---")
        self.Evaluate(self.parents, "DIRECT")

        for gen in range(numberOfGenerations):
            print(f"\n======= Generation {gen+1}/{numberOfGenerations} =======")
            self.Spawn()
            self.Mutate()
            print(f"\n--- Evaluating Children (Generation {gen+1}) ---")
            self.Evaluate(self.children, "DIRECT") # Evaluate children
            self.Print(gen) # Print combined fitness info
            self.Select() # Select based on the evaluated fitness
            print(f"======= End of Generation {gen+1} =======")

        # Clean up generated body/world files at the end
        os.system("rm body.urdf 2> /dev/null")
        os.system("rm world*.sdf 2> /dev/null")


    def Spawn(self):
        print("\n--- Spawning Children ---")
        self.children = {}
        for key in self.parents:
            child = copy.deepcopy(self.parents[key])
            child.Set_ID(self.nextAvailableID)
            self.children[key] = child # Store child with the same key as its parent
            self.nextAvailableID += 1
        print(f"Spawned {len(self.children)} children.")


    def Mutate(self):
        print("\n--- Mutating Children ---")
        for key in self.children:
            self.children[key].Mutate()
        print("Finished mutating children.")


    # This method now calls the solution's own Evaluate method
    def Evaluate(self, solutions, mode):
        for key in solutions:
             # Solution's Evaluate handles both worlds A & B and averages fitness
             solutions[key].Evaluate(mode)

        # Optional: Add a small delay here if simulations seem to overlap/interfere
        # time.sleep(1) # e.g., wait 1 second after launching all evaluations


    def Print(self, generation):
        print(f"\n--- Generation {generation+1} Results ---")
        print("ID | Parent Fitness | Child Fitness  | Better")
        print("---|----------------|----------------|--------")
        for key in self.parents:
            parent_fitness = self.parents[key].fitness
            # Check if child exists for this key (should always in this setup)
            child_fitness = self.children[key].fitness if key in self.children else float('inf')

            better = "Child" if child_fitness < parent_fitness else "Parent"
            if child_fitness == parent_fitness:
                better = "Equal"

            print(f"{key:2d} | {parent_fitness:14.4f} | {child_fitness:14.4f} | {better}")
        print("-" * 50)


    def Select(self):
        print("\n--- Performing Selection ---")
        replaced_count = 0
        for key in self.parents:
            # Check if the child exists and has better (lower) fitness
            if key in self.children and self.children[key].fitness < self.parents[key].fitness:
                self.parents[key] = self.children[key]
                replaced_count += 1
        print(f"Selected {replaced_count} children to replace parents.")


    def Show_Best(self):
        print("\n--- Determining Best Solution ---")
        bestFitness = float('inf')
        bestKey = -1
        for key in self.parents:
            if self.parents[key].fitness < bestFitness:
                bestFitness = self.parents[key].fitness
                bestKey = key

        if bestKey != -1:
             print(f"Best solution found: ID {bestKey} with Average Fitness: {bestFitness:.4f}")
             print(f"--- Running Best Solution (ID {bestKey}) in GUI Mode (World A) ---")
             best_solution = self.parents[bestKey]
             # We need to regenerate files for the best solution before simulating
             best_solution.Generate_World() # Create worldA.sdf and worldB.sdf
             best_solution.Create_Body()    # Create body.urdf
             best_solution.Create_Brain()   # Create brain<ID>.nndf
             # Start simulation in GUI mode for world A ONLY
             best_solution.Start_Single_Simulation("GUI", 'A')
             # We don't wait here - just let it run visually.
             # Add a prompt to keep the script alive while watching
             input("Press Enter to quit after viewing the simulation...")
        else:
             print("Could not determine the best solution (perhaps all fitnesses were infinite).")