import os, sys, copy

PROJECT_ROOT = os.environ['MNTR_BB_ROOT_DIR']
sys.path.append(PROJECT_ROOT)
from Parameters import msg

class TrajSafety:
    """
    Safety checker for trajectories and logs that supports multiple constraints.
    A trajectory or log sample is considered safe only if **all** constraints
    are satisfied.  Each constraint is a tuple (state_idx, op, const).

    Supported operators:
        - 'ge' : state >= const is unsafe
        - 'le' : state <= const is unsafe
        - 'gt' : state  > const is unsafe
        - 'lt' : state  < const is unsafe
    """

    def __init__(self, unsafeConstraint):
        """
        Initialize with either a single constraint [state_idx, op, const],
        or a list of such constraints.  Constraints can also be provided
        as dictionaries with keys 'state', 'state_idx', 'op', 'inequal',
        and 'const'/'value'.
        """
        constraints = []
        # If the first element is a list/tuple/dict, treat the whole arg as multiple constraints
        if isinstance(unsafeConstraint, (list, tuple)) and unsafeConstraint and isinstance(unsafeConstraint[0], (list, tuple, dict)):
            items = unsafeConstraint
        else:
            items = [unsafeConstraint]

        for item in items:
            if isinstance(item, dict):
                st = item.get('state_idx') or item.get('state')
                op = item.get('op') or item.get('inequal')
                val = item.get('const') or item.get('value')
                if st is None or op is None or val is None:
                    raise ValueError(f"Constraint dict {item!r} must define state, op, and const")
            else:
                try:
                    st, op, val = item
                except Exception:
                    raise ValueError(
                        f"Constraint {item!r} is not in a recognized format. "
                        "Expected a 3‑tuple/list or a dict with appropriate keys."
                    )
            constraints.append((int(st), op, float(val)))
        self.constraints = constraints

    def getSafeUnsafeTrajs(self, trajs):
        safeTrajs = []
        unsafeTrajs = []
        for traj in trajs:
            safeFlag, _ = self.isTrajSafe(traj)
            if safeFlag:
                safeTrajs.append(traj)
            else:
                unsafeTrajs.append(traj)
        return safeTrajs, unsafeTrajs

    def isTrajsSafe(self, trajs):
        for traj in trajs:
            safeFlag, tViolate = self.isTrajSafe(traj)
            if not safeFlag:
                return traj, tViolate
        return True, -1

    def isTrajSafe(self, traj):
        """
        Returns (True, -1) if all constraints are satisfied at every time step;
        otherwise returns (False, t) where t is the index of the first violating time step.
        """
        for t, state_vec in enumerate(traj):
            for (st_idx, op, const) in self.constraints:
                val = state_vec[st_idx]
                if op == 'ge' and val >= const:
                    print(
                        f"{msg.FAIL}[Violated]{msg.ENDC} state[{st_idx}] >= {const} at time step {t} (value: {val})"
                    )
                    return False, t
                elif op == 'le' and val <= const:
                    print(
                        f"[{msg.FAIL}Violated]{msg.ENDC} state[{st_idx}] <= {const} at time step {t} (value: {val})"
                    )
                    return False, t
                elif op == 'gt' and val > const:
                    print(
                        f"{msg.FAIL}[Violated]{msg.ENDC} state[{st_idx}] > {const} at time step {t} (value: {val})"
                    )
                    return False, t
                elif op == 'lt' and val < const:
                    print(
                        f"{msg.FAIL}[Violated]{msg.ENDC} state[{st_idx}] < {const} at time step {t} (value: {val})"
                    )
                    return False, t
        return True, -1

    def getSafeUnsafeLog(self, log):
        safeSamps = []
        unsafeSamps = []
        for sample in log:
            if self.isSampleSafe(sample):
                safeSamps.append(sample)
            else:
                unsafeSamps.append(sample)
        return safeSamps, unsafeSamps

    def isLogSafe(self, log):
        for k, sample in enumerate(log):
            if not self.isSampleSafe(sample):
                return k
        return True

    def isSampleSafe(self, sample):
        """
        Return True if all constraints are satisfied for this log sample.
        A sample is (box, t) where box is a list of [lo, hi] for each state.
        """
        box, sample_time = sample[0], sample[1]
        for (st_idx, op, const) in self.constraints:
            lo, hi = box[st_idx]
            if op == 'ge' and hi >= const:
                print(
                    f"{msg.FAIL}[Violated]{msg.ENDC} state[{st_idx}] >= {const} in log record at t={sample_time} "
                    f"(interval: [{lo}, {hi}])"
                )
                return False
            elif op == 'le' and lo <= const:
                print(
                    f"{msg.FAIL}[Violated]{msg.ENDC} state[{st_idx}] <= {const} in log record at t={sample_time} "
                    f"(interval: [{lo}, {hi}])"
                )
                return False
            elif op == 'gt' and hi > const:
                print(
                    f"{msg.FAIL}[Violated]{msg.ENDC} state[{st_idx}] > {const} in log record at t={sample_time} "
                    f"(interval: [{lo}, {hi}])"
                )
                return False
            elif op == 'lt' and lo < const:
                print(
                    f"{msg.FAIL}[Violated]{msg.ENDC} state[{st_idx}] < {const} in log record at t={sample_time} "
                    f"(interval: [{lo}, {hi}])"
                )
                return False
        return True