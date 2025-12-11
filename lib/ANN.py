import os
import numpy as np
try:
    from tensorflow.keras.models import load_model
except Exception:
    from keras.models import load_model

class ANN:
    def __init__(self, model_path: str):
        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        self.model = load_model(model_path, compile=False, safe_mode=False)
        self.input_shape = self.model.input_shape

    def prepareInput(self, state):
        arr = np.asarray(state, dtype=np.float32).reshape(-1)
        shape = self.input_shape
        if isinstance(shape, list):
            raise ValueError("Multiple input models are not supported")

        if len(shape) == 2:
            nFeatures = shape[1] or arr.size
            if arr.size != nFeatures:
                raise ValueError(f"expected {nFeatures} features, got {arr.size}")
            return arr.reshape(1, nFeatures)

        if len(shape) == 3:
            # Recurrent input: (batch, timesteps, features)
            _, timesteps, features = shape
            if features is None:
                features, timesteps = arr.size, 1
            total_expected = (timesteps or 1) * features
            if arr.size == features:
                return arr.reshape(1, 1, features)
            if arr.size == total_expected:
                return arr.reshape(1, timesteps, features)
            raise ValueError(
                f"expected {features} or {total_expected} values for "
                f"{timesteps} time steps, got {arr.size}"
            )
        raise ValueError(f"unsupported input shape {shape}")

    def getSingleState(self, state):
        x = self.prepareInput(state)
        out = self.model.predict(x, verbose=0)
        return tuple(float(v) for v in out.reshape(-1))

    def getNextState(self, init_states, T):
            
        states = [list(map(float, s)) for s in init_states]
        K = len(states)
        trajectories = [[] for _ in range(K)]
        for _ in range(T):
            # append current state to each trajectory
            for idx, st in enumerate(states):
                trajectories[idx].append(tuple(st))
            try:
                # build a batch array and predict next states
                x_batch = [self.prepareInput(st) for st in states]
                x_batch = np.concatenate(x_batch, axis=0)
                out = self.model.predict(x_batch, verbose=0)
                out_flat = out.reshape((K, -1))
                states = [list(map(float, out_flat[i])) for i in range(K)]
            except Exception:
                # fall back to one‑by‑one prediction if the batch fails
                new_states = []
                for st in states:
                    ns = list(self.getSingleState(st))
                    new_states.append(ns)
                states = new_states
        return trajectories