import numpy
import matplotlib.pyplot

backLegSensorValues = numpy.array(0)
frontLegSensorValues = numpy.array(0)
with open('data/backLegSensorValues.npy', 'rb') as f:
    backLegSensorValues = numpy.load(f)
with open('data/frontLegSensorValues.npy', 'rb') as f:
    frontLegSensorValues = numpy.load(f)

amplitude, frequency, phaseOffset = numpy.pi/4, 10, 0
targetAngles = amplitude * numpy.sin(frequency * numpy.linspace(0, 2 * numpy.pi, 1000) + phaseOffset)

matplotlib.pyplot.plot(targetAngles, label="Motor")

# matplotlib.pyplot.plot(backLegSensorValues, label="Back Leg", linewidth=6)
# matplotlib.pyplot.plot(frontLegSensorValues, label="Front Leg")

matplotlib.pyplot.legend()
matplotlib.pyplot.show()