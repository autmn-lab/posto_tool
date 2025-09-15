import os,sys,copy
import time
import ast

PROJECT_ROOT = os.environ['MNTR_BB_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

import numpy as np
try:
    from tensorflow.keras.models import load_model
except ImportError:
    from keras.models import load_model


class ANN:
      def __init__(self, model_path):
        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        self.model = load_model(model_path)

def modelNextState(self, state):

        x_cur = copy.copy(state[0])
        y_cur = copy.copy(state[1])

        inp = np.array([[x_cur, y_cur]], dtype=np.float32)  # shape (1,2)
        out = self.model.predict(inp, verbose=0).reshape(-1)

        if out.size < 2:
            raise RuntimeError("Model must output two values (x_next, y_next)")
        nextState = (float(out[0]), float(out[1]))
        return nextState