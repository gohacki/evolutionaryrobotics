import pyrosim.pyrosim as pyrosim
import random 

length, width, height = 1, 1, 1

def Create_World():
    x, y, z = -3,3,.5
    pyrosim.Start_SDF("world.sdf")

    pyrosim.Send_Cube(name="Box", pos=[x,y,z], size=[length,width,height])

    pyrosim.End()

def Generate_Body():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0,0,1.5], size=[length,width,height])
    pyrosim.Send_Cube(name="BackLeg", pos=[-.5,0,-.5], size=[length,width,height]) 
    pyrosim.Send_Cube(name="FrontLeg", pos=[.5,0,-.5], size=[length,width,height])
    pyrosim.Send_Joint( name = "Torso_BackLeg", parent = "Torso", child = "BackLeg", type = "revolute", position = [-.5,0,1])
    pyrosim.Send_Joint( name = "Torso_FrontLeg", parent = "Torso", child = "FrontLeg", type = "revolute", position = [.5,0,1])
    pyrosim.End()

def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")

      
    # NEW: Define lists of sensor and motor neurons (each tuple is (neuron_name, associated_link/joint))
    sensor_neurons = [("0", "Torso"), ("1", "BackLeg"), ("2", "FrontLeg")]  # NEW:
    motor_neurons = [("3", "Torso_BackLeg"), ("4", "Torso_FrontLeg")]         # NEW:
    
    # NEW: Send sensor neurons to the neural network
    for sensor in sensor_neurons:  # NEW:
        pyrosim.Send_Sensor_Neuron(name=sensor[0], linkName=sensor[1])  # NEW:
    
    # NEW: Send motor neurons to the neural network
    for motor in motor_neurons:  # NEW:
        pyrosim.Send_Motor_Neuron(name=motor[0], jointName=motor[1])  # NEW:
    
    # NEW: Create fully connected synapses with random weights in the range [-1, 1]
    for sensor in sensor_neurons:  # NEW:
        for motor in motor_neurons:  # NEW:
            weight = random.uniform(-1, 1)  # NEW: Random weight in [-1, 1]
            pyrosim.Send_Synapse(sourceNeuronName=sensor[0], targetNeuronName=motor[0], weight=weight)  # NEW:

    # pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
    # pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
    # pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
    # pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
    # pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")
    # # pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 3 , weight = 1.0 )
    # # pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 4 , weight = 0.5 )
    # # pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = 0.5 )
    # # pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 4 , weight = 1.0 )
    # # pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 3 , weight = -1.0 )
    # # pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = -0.5 )
    # pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 3 , weight = -1.0 )
    # pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 4 , weight = -1.0 )
    # pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = -1.0 )
    # pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 4 , weight = 0.5 )
    # pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 3 , weight = -0.5 )
    # pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = -1.0 )


    



    pyrosim.End()




Create_World()
Generate_Body()
Generate_Brain()

