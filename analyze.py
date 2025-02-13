import numpy
import matplotlib.pyplot

backLegSensorValues = numpy.array(0)
frontLegSensorValues = numpy.array(0)
with open('data/backLegSensorValues.npy', 'rb') as f:
    backLegSensorValues = numpy.load(f)
with open('data/frontLegSensorValues.npy', 'rb') as f:
    frontLegSensorValues = numpy.load(f)
matplotlib.pyplot.plot(backLegSensorValues, label="Back Leg", linewidth=6)
matplotlib.pyplot.plot(frontLegSensorValues, label="Front Leg")
matplotlib.pyplot.legend()
matplotlib.pyplot.show()