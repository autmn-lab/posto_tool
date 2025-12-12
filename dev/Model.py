#Used if the user wants to create their own custom getNextState() function insetad of using the equation or ann from the command-line.


#Add your imports
import os,sys,copy

PROJECT_ROOT = os.environ['POSTO_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

import random
import numpy as np
from System import System
from Parameters import *

def my_getNextState(state):
    
    dt=0.01
    ep=0.002

    x_cur=copy.copy(state[0])
    y_cur=copy.copy(state[1])

    x_cur+=random.uniform(0,ep)
    y_cur+=random.uniform(0,ep)

    x_next=x_cur+(dt*(-y_cur-(1.5*(x_cur)-(0.5*(x_cur*x_cur))-0.5)))
    y_next=y_cur+(dt*((3*x_cur)-y_cur))

    nextState=(x_next,y_next)
    return nextState


# no mode/model_path: we'll inject our own step function
my_states = ['x', 'y']
my_constraints = [(1, 'ge', 0.49)]
sys = System(log_path="logs/custom_with_modelpy.lg",states=my_states, constraints=my_constraints)

# override the engine step
sys.getNextState = my_getNextState

# generate a log: init set must match state dimension (x, y)
init_box = [[0.0, 0.2], [0.0, 0.2]]
sys.behaviour(init_box, T=1000)
sys.generateLog(init_box, T=2000, prob=2, dtlog=0.02)
sys.checkSafety()









