import os
import sys
import math
import numpy as np

PROJECT_ROOT = os.environ['POSTO_ROOT_DIR']
sys.path.append(PROJECT_ROOT)
from System import System
from Parameters import *

def my_getNextState1(state):
    x = np.asarray(state, dtype=np.float32).reshape(1, -1)
    u = float(sys_obj.model.model.predict(x, verbose=0)[0, 0]) 
    p_cur, v_cur = float(state[0]), float(state[1])
    p_next = p_cur + v_cur
    v_next = v_cur + 0.0015 * u - 0.0025 * math.cos(3.0 * p_cur)
    return (p_next, v_next)

def my_getNextState2(init_states, T):
    states = [list(map(float, s)) for s in init_states]
    K = len(states)
    trajectories = [[] for _ in range(K)]
    for _ in range(T):
        for idx, st in enumerate(states):
            trajectories[idx].append((st[0], st[1]))
        x_batch = np.asarray(states, dtype=np.float32)
        # Use the model loaded by System rather than a stand‑alone controller
        u_batch = sys_obj.model.model.predict(x_batch, verbose=0).reshape(K, -1)
        new_states = []
        for i in range(K):
            p_cur, v_cur = states[i]
            u_val = float(u_batch[i][0])
            p_next = p_cur + v_cur
            v_next = v_cur + 0.0015 * u_val - 0.0025 * math.cos(3.0 * p_cur)
            new_states.append([p_next, v_next])
        states = new_states
    return trajectories

# Instantiate the System and let it load the ANN from model_path
sys_obj = System(
    log_path=os.path.join('art/ANN/(d)', 'MCcontroller.lg'),
    mode='ann',
    model_path='models/MountainCar_ReluController.h5',
    states=['p', 'v'],
    constraints='models/constraints_mc.json'
)
# Override the default getNextState method
sys_obj.model.getNextState = my_getNextState2

