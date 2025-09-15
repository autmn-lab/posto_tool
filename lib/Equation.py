import os,sys,copy
import time
import ast

PROJECT_ROOT = os.environ['MNTR_BB_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

import numpy as np
import random
import json
import math

ALLOWED_FUNCS = {
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
    'fabs': math.fabs, 'abs': abs
}
eq_cache = {}

class Equation:

    def __init__(self, eq_path):
        self.func = Equation.build(eq_path)

    def getNextState(self, state):
        return self.func(state)

    @staticmethod
    def build(json_path):
        if json_path in eq_cache:
            return eq_cache[json_path]

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

        rhs_exprs = []
        for v in state_vars:
            key = f"{v}'"
            if key not in eqs:
                raise KeyError(f"{json_path}: missing equation for {key}")
            rhs_exprs.append(eqs[key].replace('^', '**'))

        safe_globals = {'__builtins__': None}
        safe_globals.update(ALLOWED_FUNCS)
        for k, v in consts.items():
            safe_globals[k] = v

        ep_lo = ep_hi = None
        if 'ep' in ranges:
            lo, hi = ranges['ep']
            lo, hi = float(lo), float(hi)
            if hi < lo:
                lo, hi = hi, lo
            ep_lo, ep_hi = lo, hi

        def step(state, t=None):
            loc = {v: float(state[i]) for i, v in enumerate(state_vars)}
            if t is not None:
                loc['t'] = float(t)
            if ep_lo is not None:
                loc['ep'] = random.uniform(ep_lo, ep_hi)
            vals = [eval(expr, safe_globals, loc) for expr in rhs_exprs]
            return tuple(float(v) for v in vals)

        eq_cache[json_path] = step
        return step
