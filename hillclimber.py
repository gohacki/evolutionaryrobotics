from solution import SOLUTION  # NEW:
from constants import numberOfGenerations  # NEW:
import copy  # NEW:

class HILL_CLIMBER:
    def __init__(self):
        self.parent = SOLUTION()  # NEW:

    def Evolve(self):  # NEW:
        # Evaluate the initial solution in DIRECT (blind) mode.
        self.parent.Evaluate("DIRECT")  # NEW:
        for currentGeneration in range(numberOfGenerations):  # NEW:
            self.Evolve_For_One_Generation()  # NEW:

    def Evolve_For_One_Generation(self):  # NEW:
        self.Spawn()           # NEW:
        self.Mutate()          # NEW:
        self.child.Evaluate("DIRECT")  # NEW: Evaluate child in DIRECT mode.
        self.Print()           # NEW: Print parent's and child's fitness.
        self.Select()          # NEW:

    def Spawn(self):  # NEW:
        self.child = copy.deepcopy(self.parent)  # NEW:

    def Mutate(self):  # NEW:
        self.child.Mutate()  # NEW:

    def Select(self):  # NEW:
        # DEBUG: Uncomment to verify fitness values:
        # print("Parent fitness:", self.parent.fitness, "Child fitness:", self.child.fitness)
        # exit()
        if self.child.fitness < self.parent.fitness:  # NEW:
            self.parent = self.child  # NEW:

    def Print(self):  # NEW:
        print("Parent fitness:", self.parent.fitness, "Child fitness:", self.child.fitness)  # NEW:

    def Show_Best(self):  # NEW:
        # Re-evaluate the final parent's behavior in GUI (heads-up) mode.
        self.parent.Evaluate("GUI")  # NEW:
