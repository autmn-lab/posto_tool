import os, sys, copy
import numpy as np
import random
import json
import math

# Root directory from environment
PROJECT_ROOT = os.environ['POSTO_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

# Allow basic math functions in equations
ALLOWED_FUNCS = {
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
    'fabs': math.fabs, 'abs': abs
}

# Cache compiled equations so repeated runs don't reparse JSON
eq_cache = {}

class Equation:
    def __init__(self, eq_path):
        self.func = Equation.build(eq_path)

    def getNextState(self, state):
        return self.func(state)

    @staticmethod
    def build(json_path):
        # Return cached function if we have already compiled this JSON
        if json_path in eq_cache:
            return eq_cache[json_path]

        # Read the JSON specification
        with open(json_path, 'r') as fp:
            spec = json.load(fp)

        if 'state_vars' not in spec:
            raise KeyError(f"{json_path}: missing 'state_vars'")
        if 'equations' not in spec:
            raise KeyError(f"{json_path}: missing 'equations'")

        state_vars = spec['state_vars']
        eqs        = spec['equations']
        consts     = spec.get('constants', {})
        ranges     = spec.get('ranges', {})

        # Prepare the right‑hand side expressions in the order of state_vars
        rhs_exprs = []
        for v in state_vars:
            key = f"{v}'"
            if key not in eqs:
                raise KeyError(f"{json_path}: missing equation for {key}")
            # Replace ^ with ** for exponentiation
            rhs_exprs.append(eqs[key].replace('^', '**'))

        # Build the "globals" dict for eval with allowed functions and constants
        safe_globals = {'__builtins__': None}
        safe_globals.update(ALLOWED_FUNCS)
        for k, v in consts.items():
            safe_globals[k] = v

        # Identify noise variables: any entry in ranges that isn't a state variable
        noise_ranges = {}
        for k, (lo, hi) in ranges.items():
            if k not in state_vars:
                lo, hi = float(lo), float(hi)
                if hi < lo:
                    lo, hi = hi, lo
                noise_ranges[k] = (lo, hi)

        # Build and return a closure that evaluates the next state
        def step(state, t=None):
            # Map each state variable to its current value
            loc = {v: float(state[i]) for i, v in enumerate(state_vars)}
            # Add time if supplied
            if t is not None:
                loc['t'] = float(t)
            # Sample each noise variable independently within its specified range
            for noise_name, (lo, hi) in noise_ranges.items():
                loc[noise_name] = random.uniform(lo, hi)
            try:
                # Evaluate each RHS expression in order
                vals = [eval(expr, safe_globals, loc) for expr in rhs_exprs]
                return tuple(float(v) for v in vals)
            except OverflowError:
                # If overflow occurs, return None (used by System to stop simulation)
                return None

        # Cache and return the compiled function
        eq_cache[json_path] = step
        return step
