import numpy
import constants as c
import pyrosim.pyrosim as pyrosim

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(c.ITERATIONS)
    
    def Get_Value(self, i):
        self.values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

        # if i == c.ITERATIONS - 1:
        #     print(self.values)
    
    def Save_Values(self):
        import numpy as np
        np.save('data/{}_SensorValues.npy'.format(self.linkName), self.values)


