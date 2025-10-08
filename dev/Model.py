#Used if the user wants to create their own custom getNextState() function insetad of using the equation or ann from the command-line.


#Add your imports
import os,sys,copy

PROJECT_ROOT = os.environ['MNTR_BB_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

import random
import numpy as np
from System import *



def my_getNextState(state):

    dt=0.01
    ep=0.002
    
    x_cur=copy.copy(state[0])
    y_cur=copy.copy(state[1])
    z_cur=copy.copy(state[2])
    a_cur=copy.copy(state[3])

    x_cur+=random.uniform(0,ep)
    y_cur+=random.uniform(0,ep)
    z_cur+=random.uniform(0,ep)
    a_cur+=random.uniform(0,ep)

    x_next=x_cur+(dt*(-y_cur-(1.5*(x_cur*x_cur)-(0.5*(x_cur*x_cur*x_cur))-0.5)+(a_cur**2)));
    y_next=y_cur+(dt*((3*x_cur)-y_cur))
    z_next=z_cur+(dt*((0.1*(x_cur**2))+(0.5*(y_cur**3))+z_cur+a_cur))
    #z_next=z_cur*dt+(((0.1*(x_cur**2))+(0.5*(y_cur**3))+z_cur+a_cur))
    a_next=a_cur+(dt*(y_cur**2))
    nextState=(x_next,y_next,z_next,a_next)
    print(nextState)
    return nextState


s = System("/home/prachi-bhattacharjee/Posto/logs/customModel2.lg")
s.getNextState = my_getNextState
s.generateLog([[-0.001,0.001], [-0.001,0.001], [-0.001,0.010],[-0.001,0.001]], 100, 10, 0.1)














