#Used if the user wants to create their own custom getNextState() function insetad of using the equation or ann from the command-line.


#Add your imports
import os,sys,copy

PROJECT_ROOT = os.environ['MNTR_BB_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

import random
import numpy as np
from math import cos, sin
from System import *

def my_getNextState(state):
    c = 1
    
    x1 = float(copy.copy(state[0]))

    nextState = x1**3 + c

    
    return (nextState,)


# no mode/model_path: we'll inject our own step function
my_states = ['x']
sys = System(log_path="/home/prachi-bhattacharjee/Posto/logs/Testcode.lg")

# override the engine step
sys.getNextState = my_getNextState

# generate a log: init set must match state dimension (x, y)
init_box = [[1, 2]]
sys.behaviour(init_box, T=2000)









