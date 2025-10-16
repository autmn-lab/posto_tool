#comprehensive test suite with multiple dimensions, uncertainities injected in multiple places, multiple degrees.

#!/usr/bin/env python3
"""
Posto: Scripts to generate logs and check safety of trajectories

This tool provides two main commands: `generateLog` and `checkSafety`.
Both commands require a mode (`--mode`) and a corresponding model file (`--model_path`).

Usage:
    posto.py behavior --log=<logfile> --init=<initialState> --timestamp=<timestamp> --mode=<mode> --model_path=<model_path>
    posto.py generateLog --log=<logfile> --init=<initialState> --timestamp=<timestamp> --mode=<mode> --model_path=<model_path> --prob=<prob> --dtlog=<dtlog>
    posto.py checkSafety --log=<logfile> --mode=<mode> --model_path=<model_path>

Options:
    --log=<logfile>        Path to the log file to read from or write to.
                           For `generateLog`, this is where the generated log will be stored.
                           For `checkSafety`, this is the log to be checked.

    --init=<initialState>  [generateLog only] Initial set for log generation.
                           Must be provided in the format: "[x_min, x_max],[y_min, y_max]"
                           Example: --init="[0.8,1],[0.8,1]"

    --timestamp=<timestamp>
                           Time horizon (integer, >= 0) for the simulation.

    --mode=<mode>          The mode to use to generate the log/trajectories. Must be one of:
                             - equation : uses an equation-based function provided in the json file (.json)
                             - ann      : uses an artificial neural network model (.h5)

    --model_path=<model_path>     Path to the model file corresponding to the chosen operation:
                             - if -mode=equation → must be a .json file conatining the function.
                             - if --mode=ann      → must be a .h5 file of the trained ann model
                           The file must exist and be accessible.


Commands:
    generateLog            Generates a trajectory log based on the given initial set, time horizon,
                           and operator. The output is written to the file specified by --log.

    checkSafety            Checks whether the trajectories in the log satisfy the given safety condition.
                           The condition is specified by --state, --op, and --unsafe.

Examples:
    # Generate a log using an ANN operator
    posto.py generateLog --log=traj.log --init="[0.8,1],[0.8,1]" --timestamp=50 --mode=ann --model_path=model_path.h5

    # Generate a log using an equation operator
    posto.py generateLog --log=traj.log --init="[0.5,0.9],[0.5,0.9]" --timestamp=30 --mode=equation --model_path=operator.json

    # Check safety of a log
    posto.py checkSafety --log=traj.log --mode=ann --model_path=model_path.h5
"""


from docopt import docopt
import ast, os, sys, time, re
from System import *


def parse_initset(init_str):
    """
    Parse --init into a list of [lo, hi] float pairs for n dimensions.

    Accepts formats like:
      "[[0.8, 1.0], [0.8, 1.0], [0.8, 1.0]]"
      "[0.8, 1.0], [0.8, 1.0], [0.8, 1.0]"   (no outer brackets)
      " [  [0.8,1], [0.8,1] ]  "             (extra spaces/newlines)

    Returns:
      List[List[float, float]]

    Raises:
      ValueError with a helpful message if input is malformed.
    """
    if init_str is None:
        raise ValueError("--init is required")

    s = init_str.strip()

    # Sometimes users paste "init=..." — strip that if present
    s = re.sub(r'^\s*init\s*=\s*', '', s, flags=re.IGNORECASE).strip()

    # First try parsing as-is
    def _try_eval(txt):
        try:
            return ast.literal_eval(txt)
        except Exception:
            return None

    obj = _try_eval(s)

    # If that fails, try wrapping in outer brackets (handles no-outer-brackets case)
    if obj is None:
        obj = _try_eval(f'[{s}]')
        if obj is None:
            raise ValueError(
                "Could not parse --init. Expected something like: "
                "'[[lo, hi], [lo, hi], ...]' or '[lo, hi], [lo, hi]'. "
                f"Got: {init_str!r}"
            )

    # Normalize tuples to lists
    if isinstance(obj, tuple):
        obj = list(obj)

    # If user provided a single pair like [lo, hi], wrap it to make [[lo, hi]]
    if (isinstance(obj, list)
        and len(obj) == 2
        and all(isinstance(x, (int, float)) for x in obj)):
        obj = [obj]

    # Validate structure: list of pairs
    if not (isinstance(obj, list) and all(
        isinstance(p, (list, tuple)) and len(p) == 2 for p in obj
    )):
        raise ValueError(
            "Parsed --init is not a list of [lo, hi] pairs. "
            f"Got: {obj!r}"
        )

    # Coerce to floats and validate ordering
    out = []
    for i, pair in enumerate(obj, start=1):
        lo, hi = pair
        try:
            lo_f = float(lo)
            hi_f = float(hi)
        except Exception:
            raise ValueError(
                f"--init pair #{i} contains non-numeric values: {pair!r}"
            )
        if lo_f > hi_f:
            raise ValueError(
                f"--init pair #{i} has lo > hi: {lo_f} > {hi_f}"
            )
        out.append([lo_f, hi_f])
    if len(out) == 0:
        raise ValueError("--init parsed to an empty list of ranges")
    return out


def require_path(path_str, flag_name="--log"):
    if path_str is None or str(path_str).strip() == "":
        die(f"Missing {flag_name}.",
            hint=f"Provide a valid path via {flag_name}=<file>.")

    # Ensure parent directory exists (if one is specified)
    parent = os.path.dirname(os.path.abspath(path_str))
    if parent and not os.path.isdir(parent):
        die(f"Directory does not exist for {flag_name}: {parent!r}.",
            hint="Create the directory or change the path.")

    # Enforce file extension
    if not str(path_str).endswith(".lg"):
        die(f"Invalid file type for {flag_name}: {path_str!r}.",
            hint="The log file must use the .lg extension.")

    return path_str

def require_int(val_str, flag_name, min_value=None, max_value=None):
    if val_str is None:
        die(f"Missing {flag_name}.",
            hint=f"Provide an integer via {flag_name}=<int>.")
    try:
        v = int(val_str)
    except Exception:
        die(f"{flag_name} must be an integer (got {val_str!r}).")
    if min_value is not None and v < min_value:
        die(f"{flag_name} must be >= {min_value} (got {v}).")
    if max_value is not None and v > max_value:
        die(f"{flag_name} must be <= {max_value} (got {v}).")
    return v

def require_float(val_str, flag_name, min_value=None, max_value=None):
    if val_str is None:
        die(f"Missing {flag_name}.",
            hint=f"Provide a number via {flag_name}=<float>.")
    try:
        v = float(val_str)
    except Exception:
        die(f"{flag_name} must be a number (got {val_str!r}).")
    if min_value is not None and v < min_value:
        die(f"{flag_name} must be >= {min_value} (got {v}).")
    if max_value is not None and v > max_value:
        die(f"{flag_name} must be <= {max_value} (got {v}).")
    return v

def require_op(op_str):
    """
    Accept symbols or words; normalize to the word form used by TrajSafety:
      lt (<), le (<=), gt (>), ge (>=), eq (==), ne (!=)
    """
    if op_str is None:
        die("Missing --op.", hint="Use one of: <, <=, >, >=, ==, !=, lt, le, gt, ge, eq, ne")

    s = op_str.strip().lower()
    alias = {
        "<": "lt", "<=": "le", ">": "gt", ">=": "ge", "==": "eq", "!=": "ne",
        "lt": "lt", "le": "le", "gt": "gt", "ge": "ge", "eq": "eq", "ne": "ne",
    }
    if s not in alias:
        die(f"Invalid --op: {op_str!r}.",
            hint="Allowed: <, <=, >, >=, ==, != or lt, le, gt, ge, eq, ne")
    return alias[s]


def require_mode(mode_str):
    """
    Require --mode to be either 'equation' or 'ann' (case-insensitive).
    Returns normalized lowercase value.
    """
    if mode_str is None:
        die("Missing --mode.",
            hint='Use --mode=equation or --mode=ann')
    mode_norm = mode_str.strip().lower()
    if mode_norm not in {"equation", "ann"}:
        die(f"Invalid --mode: {mode_str!r}.",
            hint='Allowed values: "equation" or "ann"')
    return mode_norm


def require_model(model_str, mode):
    """
    Require --model_path to exist and have extension based on mode
      - ann       -> .h5
      - equation  -> .txt
    """
    if model_str is None or str(model_str).strip() == "":
        die("Missing --model_path.",
            hint="Provide a path via --model_path=<file> matching the mode.")
    path = os.path.abspath(model_str)
    if not os.path.isfile(path):
        die(f"--model_path not found: {model_str!r}.",
            hint="Check the path and permissions.")
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    if mode == "ann" and ext != ".h5":
        die(f"--model_path must be a .h5 file for mode 'ann' (got {ext}).")
    if mode == "equation" and ext != ".json":
        die(f"--model_path must be a .json file for mode 'equation' (got {ext}).")
    return path



# ---------- main ----------
if __name__ == '__main__':
    args = docopt(__doc__)

    log = require_path(args['--log'], "--log")
    mode = require_mode(args['--mode'])
    model_path = require_model(args['--model_path'], mode)

    my_sys = System(log, mode, model_path)

    if args['behavior']:
        init = parse_initset(args['--init'])
        timestamp = require_int(args['--timestamp'], "--timestamp", min_value=0)
        my_sys.behaviour(init, timestamp)
        

    elif args['generateLog']:
        init = parse_initset(args['--init'])
        timestamp = require_int(args['--timestamp'], "--timestamp", min_value=0)
        prob = require_float(args['--prob'], "--prob", min_value=0)
        dtlog = require_float(args['--dtlog'], "--dtlog", min_value=0)

        
        try:
            my_sys.generateLog(init, timestamp, prob, dtlog)
        except Exception as e:
            die(f"Log generation failed: {e!r}",
                hint="Check your inputs and file permissions.")

    elif args['checkSafety']:
        try:
            my_sys.checkSafety()
            ok("Safety check completed.")
        except Exception as e:
            die(f"Safety check failed: {e!r}",
                hint="Verify the log file exists and input parameters are correct.")
    else:
        warn("No command provided. Use 'generateLog' or 'checkSafety'.")
        print(__doc__)
        sys.exit(1)
