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
        self.model = load_model(model_path, compile=False, safe_mode=False)

def getNextState(self, state):


        out = self.model.predict(state, verbose=0).reshape(-1)

        nextState = out
        return nextState