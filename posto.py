#!/usr/bin/env python3
"""
Posto: scripts to generate logs, plot behaviour trajectories and check safety
of trajectories.

Usage:
    posto.py behavior --log=<directory> --init=<initialSet> --timestamp=<T> --mode=<mode> --model_path=<model_path> [--states=<states>]
    posto.py generateLog --log=<logfile> --init=<initialSet> --timestamp=<T> --mode=<mode> --model_path=<model_path> --prob=<prob> --dtlog=<dtlog> [--states=<states>]
    posto.py checkSafety --log=<logfile> --mode=<mode> --model_path=<model_path> [--states=<states>] [--constraints=<constraints>]

Options:
    --log=<directory or logfile>   For `behavior`, path to a directory where plots will be saved; an `img` folder will be created under this directory.
                                   For `generateLog` and `checkSafety`, path to the `.lg` file to write or read; plots are saved in an `img` folder next to the file.
    --init=<initialSet>            Initial state set for trajectory sampling, e.g. "[0.8,1],[0.8,1]".  One [lo, hi] pair per dimension.
    --timestamp=<T>                Time horizon (integer ≥ 0) for the simulation.
    --mode=<mode>                  Either `equation` (use a JSON model) or `ann` (use a trained neural network `.h5`).
    --model_path=<model_path>      Path to the model file (.json for equation, .h5 for ann).
    --prob=<prob>                  Probability of logging at each step when generating a log (float ≥ 0).
    --dtlog=<dtlog>                Time step between logged entries when generating a log (float ≥ 0).
    --states=<states>              Comma-separated list of state variable names.  Required for ann mode; optional for equation mode.
    --constraints=<constraints>    Safety constraints specification (JSON file or list).  Required for checkSafety in ann mode; optional otherwise.

Examples:
    # Plot random trajectories using an ANN model and save plots to ./plots/img
    posto.py behavior --log=./plots --init="[0.8,1],[0.8,1]" --timestamp=50 --mode=ann --model_path=model.h5 --states=x,y

    # Generate a trajectory log using an equation model
    posto.py generateLog --log=traj.lg --init="[0.5,0.9],[0.5,0.9]" --timestamp=30 --mode=equation --model_path=operator.json --prob=0.2 --dtlog=0.1

    # Check safety of an existing log
    posto.py checkSafety --log=traj.lg --mode=ann --model_path=model.h5 --states=x,y --constraints=constraints.json
"""

from docopt import docopt
import ast
import os
import re
import sys

from System import *
from Parameters import die, ok, warn


def parse_initset(init_str):
    """Convert a string like "[0,1],[2,3]" into a list of [lo, hi] pairs."""
    if init_str is None:
        raise ValueError("--init is required")
    s = init_str.strip()
    s = re.sub(r'^\s*init\s*=\s*', '', s, flags=re.IGNORECASE).strip()

    def _try_eval(txt):
        try:
            return ast.literal_eval(txt)
        except Exception:
            return None

    obj = _try_eval(s)
    if obj is None:
        obj = _try_eval(f'[{s}]')
        if obj is None:
            raise ValueError(
                "Could not parse --init. Expected something like '[lo, hi],[lo, hi]'."
            )
    if isinstance(obj, tuple):
        obj = list(obj)
    if isinstance(obj, list) and len(obj) == 2 and all(isinstance(x, (int, float)) for x in obj):
        obj = [obj]
    if not (isinstance(obj, list) and all(isinstance(p, (list, tuple)) and len(p) == 2 for p in obj)):
        raise ValueError("--init is not a list of [lo, hi] pairs.")
    out = []
    for pair in obj:
        lo, hi = pair
        try:
            lo_f = float(lo)
            hi_f = float(hi)
        except Exception:
            raise ValueError(f"--init contains non‑numeric values: {pair!r}")
        if lo_f > hi_f:
            raise ValueError(f"--init lower bound > upper bound: {pair!r}")
        out.append([lo_f, hi_f])
    if not out:
        raise ValueError("--init parsed to an empty list of ranges")
    return out


def require_path(path_str, flag_name="--log"):
    """Ensure that path_str is a .lg file and its parent directory exists."""
    if path_str is None or str(path_str).strip() == "":
        die(f"Missing {flag_name}.", hint=f"Provide a valid path via {flag_name}=<file>.")
    parent = os.path.dirname(os.path.abspath(path_str))
    if parent and not os.path.isdir(parent):
        die(f"Directory does not exist for {flag_name}: {parent!r}.",
            hint="Create the directory or change the path.")
    if not str(path_str).endswith(".lg"):
        die(f"Invalid file type for {flag_name}: {path_str!r}.",
            hint="The log file must use the .lg extension.")
    return path_str


def require_int(val_str, flag_name, min_value=None, max_value=None):
    if val_str is None:
        die(f"Missing {flag_name}.", hint=f"Provide an integer via {flag_name}=<int>.")
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
        die(f"Missing {flag_name}.", hint=f"Provide a number via {flag_name}=<float>.")
    try:
        v = float(val_str)
    except Exception:
        die(f"{flag_name} must be a number (got {val_str!r}).")
    if min_value is not None and v < min_value:
        die(f"{flag_name} must be >= {min_value} (got {v}).")
    if max_value is not None and v > max_value:
        die(f"{flag_name} must be <= {max_value} (got {v}).")
    return v


def require_mode(mode_str):
    if mode_str is None:
        die("Missing --mode.", hint='Use --mode=equation or --mode=ann')
    m = mode_str.strip().lower()
    if m not in {"equation", "ann"}:
        die(f"Invalid --mode: {mode_str!r}.", hint='Allowed values: "equation" or "ann"')
    return m


def require_model(model_str, mode):
    if model_str is None or str(model_str).strip() == "":
        die("Missing --model_path.", hint="Provide a path via --model_path=<file> matching the mode.")
    path = os.path.abspath(model_str)
    if not os.path.isfile(path):
        die(f"--model_path not found: {model_str!r}.", hint="Check the path and permissions.")
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    if mode == "ann" and ext != ".h5":
        die(f"--model_path must be a .h5 file for mode 'ann' (got {ext}).")
    if mode == "equation" and ext != ".json":
        die(f"--model_path must be a .json file for mode 'equation' (got {ext}).")
    return path


if __name__ == '__main__':
    args = docopt(__doc__)

    # Extract common CLI values
    log_arg = args['--log']
    mode = require_mode(args['--mode'])
    model_path = require_model(args['--model_path'], mode)
    states = args['--states'].split(',') if args['--states'] else None
    constraints = args['--constraints'] if args['--constraints'] else None

    # For ANN mode, require both state names and constraints
    if mode == 'ann':
        if not states:
            die("Missing --states for ann mode.", hint="Provide state names via --states=<name1,name2,...>.")
        if args['checkSafety'] and not constraints:
            die("Missing --constraints for ann mode.", hint="Provide constraints via --constraints=<json or list>.")

    # Interpret --log depending on the command
    if args['behavior']:
        # Behavior uses a directory; no .lg suffix is required
        log = log_arg
    else:
        # generateLog and checkSafety require a .lg log file
        log = require_path(log_arg, "--log")

    # Create the System instance
    my_sys = System(log, mode, model_path, states, constraints)

    # Dispatch to the appropriate command with consistent error handling
    if args['behavior']:
        init = parse_initset(args['--init'])
        timestamp = require_int(args['--timestamp'], "--timestamp", min_value=0)
        try:
            my_sys.behaviour(init, timestamp)
            ok("Behavior generation completed.")
        except Exception as e:
            die(f"Behavior generation failed: {e!r}", hint="Check your inputs and file permissions.")
    elif args['generateLog']:
        init = parse_initset(args['--init'])
        timestamp = require_int(args['--timestamp'], "--timestamp", min_value=0)
        prob = require_float(args['--prob'], "--prob", min_value=0)
        dtlog = require_float(args['--dtlog'], "--dtlog", min_value=0)
        try:
            my_sys.generateLog(init, timestamp, prob, dtlog)
            ok("Log generation completed.")
        except Exception as e:
            die(f"Log generation failed: {e!r}", hint="Check your inputs and file permissions.")
    elif args['checkSafety']:
        try:
            my_sys.checkSafety()
            ok("Safety check completed.")
        except Exception as e:
            die(f"Safety check failed: {e!r}",
                hint="Verify the log file exists and input parameters are correct.")
    else:
        warn("No command provided. Use 'behavior', 'generateLog' or 'checkSafety'.")
        print(__doc__)
        sys.exit(1)
