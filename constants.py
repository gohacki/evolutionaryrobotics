import numpy
import random
GRAVITY = -9.8
ITERATIONS = 1000
AMPLITUDE = numpy.pi/4
FREQUENCY = 30
PHASEOFFSET = 0
AMPLITUDE2 = numpy.pi/4
FREQUENCY2 = 30
PHASEOFFSET2 = numpy.pi/2
RANGESTART = 0
RANGEEND = numpy.pi*2
SLEEPTIME = 1/60
MAXFORCE= 200

numberOfGenerations = 10
populationSize = 10

numSensorNeurons = 4
numMotorNeurons = 8

motorJointRange = .2

def _get_random_box_position():
    """Generates a random box position according to the original logic."""
    # Randomly choose which side (negative or positive x)
    if random.random() < 0.5:
        # Negative side: x between -5.0 and -3.0
        x = random.uniform(-5.0, -3.0)
    else:
        # Positive side: x between 3.0 and 5.0
        x = random.uniform(3.0, 5.0)

    # Randomly choose which side (negative or positive y)
    if random.random() < 0.5:
        # Negative side: y between -5.0 and -3.0
        y = random.uniform(-5.0, -3.0)
    else:
        # Positive side: y between 3.0 and 5.0
        y = random.uniform(3.0, 5.0)
    z = 0.5
    return [x, y, z]

# Generate the position ONCE when the module is imported
FIXED_BOX_POSITION = _get_random_box_position()