#!/usr/bin/env python3
"""
Posto: Scripts to generate logs and check safety of trajectories

This tool provides two main commands: `generateLog` and `checkSafety`.
Both commands require a mode (`--mode`) and a corresponding model file (`--model_path`).

Usage:
    posto.py generateLog --log=<logfile> --init=<initialState> --timestamp=<timestamp> --mode=<mode> --model_path=<model_path> --prob=<prob> --dtlog=<dtlog>
    posto.py checkSafety --log=<logfile> --timestamp=<timestamp> --mode=<mode> --model_path=<model_path> --unsafe=<unsafe> --state=<state> --op=<op>

Options:
    --log=<logfile>        Path to the log file to read from or write to.
                           For `generateLog`, this is where the generated log will be stored.
                           For `checkSafety`, this is the log to be checked.

    --init=<initialState>  [generateLog only] Initial set for log generation.
                           Must be provided in the format: "[x_min, x_max],[y_min, y_max]"
                           Example: --init="[0.8,1],[0.8,1]"

    --timestamp=<timestamp>
                           Time horizon (integer, >= 0) for the simulation or safety check.

    --mode=<mode>          The mode to use to generate the log/trajectories. Must be one of:
                             - equation : uses an equation-based function provided in the json file (.json)
                             - ann      : uses an artificial neural network model (.h5)

    --model_path=<model_path>     Path to the model file corresponding to the chosen operation:
                             - if -mode=equation → must be a .json file conatining the function.
                             - if --mode=ann      → must be a .h5 file of the trained ann model
                           The file must exist and be accessible.

    --unsafe=<unsafe>      [checkSafety only] Unsafe threshold value (float).

    --state=<state>        [checkSafety only] Index of the state variable to evaluate (integer, >= 0).

    --op=<op>              [checkSafety only] Operator used in the safety condition.
                           Accepted forms:
                             - Symbolic: <, <=, >, >=, ==, !=
                             - Word form: lt, le, gt, ge, eq, ne
                           Example: --op=le   (equivalent to <=)

Commands:
    generateLog            Generates a trajectory log based on the given initial set, time horizon,
                           and operator. The output is written to the file specified by --log.

    checkSafety            Checks whether the trajectories in the log satisfy the given safety condition.
                           The condition is specified by --state, --op, and --unsafe.

Examples:
    # Generate a log using an ANN operator
    posto.py generateLog --log=traj.log --init="[0.8,1],[0.8,1]" --timestamp=50 --mode=ann --model_path=model_path.h5

    # Generate a log using an equation operator
    posto.py generateLog --log=traj.log --init="[0.5,0.9],[0.5,0.9]" --timestamp=30 --mode=equation --model_path=operator.txt

    # Check safety of a log
    posto.py checkSafety --log=traj.log --timestamp=50 --mode=ann --model_path=model_path.h5 --unsafe=0.5 --state=1 --op=le
"""


from docopt import docopt
import ast, os, sys, time
from System import *

# ---------- helpers: colored logging ----------
def info(s):    print(f"{msg.OKCYAN}[INFO]{msg.ENDC} {s}")
def note(s):    print(f"{msg.OKBLUE}[INFO]{msg.ENDC} {s}")
def ok(s):      print(f"{msg.OKGREEN}[SUCCESS]{msg.ENDC} {s}")
def warn(s):    print(f"{msg.WARNING}[WARN]{msg.ENDC} {s}")
def die(s, hint=None, code=2):
    print(f"{msg.FAIL}[ERROR]{msg.ENDC} {s}")
    if hint:
        print(f"{msg.WARNING}[HINT]{msg.ENDC} {hint}")
    sys.exit(code)

# ---------- parsing & validation ----------
def parse_initset(init_str):
    """
    Accepts formats like:
      "[0.8,1],[0.8,1]"
      " [ 0.8 , 1.0 ] , [ 0.8 , 1.0 ] "
    Returns: ([x1,x2], [y1,y2]) as floats
    """
    if init_str is None:
        die("Missing --init.",
            hint='Provide it in format: "[0.8,1],[0.8,1]"')

    try:
        parts = init_str.split("],")
        if len(parts) != 2:
            raise ValueError("Expected two bracketed ranges separated by a comma.")
        set1 = ast.literal_eval(parts[0].strip() + "]")
        set2 = ast.literal_eval(parts[1].strip())
        if (not isinstance(set1, (list, tuple)) or len(set1) != 2 or
            not isinstance(set2, (list, tuple)) or len(set2) != 2):
            raise ValueError("Each set must have exactly two numbers.")
        set1 = [float(set1[0]), float(set1[1])]
        set2 = [float(set2[0]), float(set2[1])]
        return (set1, set2)
    except Exception as e:
        die(
            f"Invalid --init format: {init_str!r}.",
            hint='Use like: "[0.8,1],[0.8,1]" (two bracketed pairs separated by a comma).'
        )

def require_path(path_str, flag_name="--log"):
    if path_str is None or str(path_str).strip() == "":
        die(f"Missing {flag_name}.",
            hint=f"Provide a valid path via {flag_name}=<file>.")
    # Ensure parent directory exists (if one is specified)
    parent = os.path.dirname(os.path.abspath(path_str))
    if parent and not os.path.isdir(parent):
        die(f"Directory does not exist for {flag_name}: {parent!r}.",
            hint="Create the directory or change the path.")
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

    if args['generateLog']:
        init = parse_initset(args['--init'])
        timestamp = require_int(args['--timestamp'], "--timestamp", min_value=0)
        prob = require_float(args['--prob'], "--prob", min_value=0)
        dtlog = require_float(args['--dtlog'], "--dtlog", min_value=0)


        info("Starting log generation...")
        note(f"Initial set: {init}")
        note(f"Time horizon: {timestamp}")
        note(f"Mode: {mode}")
        note(f"Model file: {model_path}")
        note(f"Logging probability: {prob}")
        note(f"Delta log: {dtlog}")
        note(f"Output log path: {log}")
        

        start = time.time()
        try:
            my_sys.generateLog(init, timestamp, prob, dtlog)
        except Exception as e:
            die(f"Log generation failed: {e!r}",
                hint="Check your inputs and file permissions.")
        elapsed = time.time() - start

        ok("Log generated successfully.")
        ok(f"Stored at: {msg.UNDERLINE}{log}{msg.ENDC}")
        print(f"{msg.HEADER}[INFO]{msg.ENDC} Time taken: {msg.BOLD}{elapsed:.4f} sec{msg.ENDC}")

    elif args['checkSafety']:
        timestamp = require_int(args['--timestamp'], "--timestamp", min_value=0)
        unsafe = require_float(args['--unsafe'], "--unsafe")
        state = require_int(args['--state'], "--state", min_value=0)
        op = require_op(args['--op'])

        info("Running safety check...")
        note(f"Log path: {log}")
        note(f"Time horizon: {timestamp}")
        note(f"Unsafe threshold: {unsafe}")
        note(f"State index: {state}")
        note(f"Operator: {op}")
        note(f"Mode: {mode}")
        note(f"Model File: {model_path}")

        try:
            my_sys.checkSafety(timestamp, unsafe, state, op)
            ok("Safety check completed.")
        except Exception as e:
            die(f"Safety check failed: {e!r}",
                hint="Verify the log file exists and input parameters are correct.")

    else:
        warn("No command provided. Use 'generateLog' or 'checkSafety'.")
        print(__doc__)
        sys.exit(1)
