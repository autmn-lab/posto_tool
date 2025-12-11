# `Posto` 

## About The Tool

With the increasing autonomous capabilities of cyber-physical systems, the complexity of their models also increases significantly, thus continually posing challenges to existing formal methods for safety verification. In contrast to model checking, monitoring emerges as an effective lightweight, yet practical verification technique capable of delivering results of practical importance with better scalability. Monitoring involves analyzing logs from an actual system to determine whether a specification (such as a safety property) is violated.  Although current monitoring techniques work well in some areas, it has largely been unable to cope with the growing complexity of the models. Monitoring techniques, such as those using reachability methods, may fail to produce results when dealing with complex models like Deep Neural Networks (DNNs). We propose here a novel statistical approach for monitoring that is able to generate results with high probabilistic guarantees. 

`Posto` is a Python-based prototype tool that implements the proposed statistical monitoring technique, enabling an effective monitoring of complex systems, including non-linear systems with DNN-based components, while providing results with high probabilistic guarantees.

`Posto` provides three main command-line operations:

1. `behavior` – draw multiple random trajectories and visualise system evolution under uncertainty.  
2. `generateLog` – simulate one trajectory, probabilistically sample it, and save it as a .lg log for later analysis.  
3. `checkSafety` – verify whether logged trajectories satisfy user-defined safety constraints.

`Posto` supports three model types:

- `Equation mode` – update equations supplied through a `JSON` model.  

- `ANN mode` – system dynamics represented by a trained `.h5` neural network model.  

- `Development mode (dev)` – supply a custom Python `getNextState` function without modifying core files.

  

  ![Overview](https://github.com/bineet-coderep/monitor-bb/blob/main/figs/Overview.png)


  ## 

## Installation

### Dependencies

- [`Python 3.9.x`](https://www.python.org/)

  - To install this on Ubuntu, one can follow the following steps (note: this step requires the user to have `sudo` privileges):

    ```bash
    sudo apt update
    sudo apt install python3.9 python3.9-venv python3.9-dev -y
    ```

- [`NumPy`](https://numpy.org/)

  ```bash
  pip install numpy
  ```

- [`SciPy`](https://scipy.org/)

  ```bash
  pip install scipy
  ```

- [`mpmath`](https://mpmath.org/)

  ```bash
  pip install mpmath
  ```

- [`mpl_toolkits`](https://matplotlib.org/2.2.2/mpl_toolkits/index.html)

  ```bash
  pip install matplotlib
  ```

- [`tqdm`](https://pypi.org/project/tqdm/2.2.3/)

  ```bash
  pip install tqdm
  ```

- [`TensorFlow`](https://www.tensorflow.org/) (required for ANN mode)

  ```bash
  pip install tensorflow
  ```

- [`docopt`](https://pypi.org/project/docopt/) (for command-line argument parsing)

  ```bash
  pip install docopt
  ```

#### Verify Installation

* To verify if the above dependencies are correctly installed, one can run the following:

  ```bash
  python -c "import numpy, scipy, mpmath, tqdm, mpl_toolkits, tensorflow, docopt; print('All dependencies installed successfully')"
  ```

* If all the dependencies are correctly installed, the above command should run without any error, and display `All dependencies installed successfully` in the terminal.

### Downloading the tool

1. Download the repository to your desired location `/path/to/Posto`

2. Once the repository is downloaded, the user needs to set the variable `POSTO_ROOT_DIR=` to `/path/to/Posto`. To do so, we recommend adding this to `bashrc` (see **Step 2.1**). For users who do not wish to add it to their `bashrc`, can set the variable each time they open the terminal session to run the tool (see **Step 2.2**). Users choosing step 2.2 are gently reminded to perform this step every time they intend to run the tool.

   1. ***[Recommended]*** Once the repository is downloaded, please open `~/.bashrc`, and add the line `export POSTO_ROOT_DIR=/path/to/Posto`, mentioned in the following steps:

      1. ```shell
         vi ~/.baschrc
         ```

      2. Once `.bashrc` is opened, please add the location, where the tool was downloaded, to a path variable `POSTO_ROOT_DIR` (This step is crucial to run the tool):

         1. ```shell
            export POSTO_ROOT_DIR=/path/to/Posto
            ```

   2. *[Alternate Approach]* Run this command every time a new terminal session is opened to run the tool:

      1. ```shell
         export POSTO_ROOT_DIR=/path/to/Posto
         ```

         

## Command-Line Usage

All operations use:
```
python posto.py <operation> [arguments]
```

| Argument                       | Required In                                                | Description                                                  |
| ------------------------------ | ---------------------------------------------------------- | ------------------------------------------------------------ |
| `--log=<directory or logfile>` | `behavior`, `generateLog`, `checkSafety`                   | **Behavior:** path to a **directory** where plots will be saved; an `img/` folder is created inside it.  **GenerateLog / CheckSafety:** path to the **.lg logfile** to write or read; plots are saved in an `img/` folder next to the logfile. |
| `--init=<initialSet>`          | `behavior`, `generateLog`                                  | Initial set for state sampling, e.g., `"[0.8,1],[0.8,1]"`. One `[lo, hi]` pair per dimension. |
| `--timestamp=<T>`              | `behavior`, `generateLog`                                  | Time horizon for the simulation (integer ≥ 0).               |
| `--mode=<mode>`                | All commands                                               | Specifies model type:  • `equation` — load system from a JSON equation model  • `ann` — load system from a `.h5` neural network model |
| `--model_path=<model_path>`    | All commands                                               | Path to model file. Use `.json` for equation mode and `.h5` for ann mode. |
| `--prob=<prob>`                | `generateLog`                                              | Logging probability per step during log generation (float ≥ 0). |
| `--dtlog=<dtlog>`              | `generateLog`                                              | Time interval between logged entries when generating a log (float ≥ 0). |
| `--states=<states>`            | Optional in equation mode; required in ann mode            | Comma-separated list of state variable names. Needed for mapping ANN inputs/outputs. |
| `--constraints=<constraints>`  | Required in `checkSafety` for ann mode; optional otherwise | Safety constraint specification (JSON file or inline list).  |

## 1. Behavior Mode

Generate random trajectories and visualise projections.

```
posto.py behavior \
    --log=<directory> \
    --init=<initialSet> \
    --timestamp=<T> \
    --mode=<mode> \
    --model_path=<model_path> \
    [--states=<states>]
```

## 2. Generate Log
Simulate a single trajectory, apply probabilistic sampling, and store it in a .lg file.

```
posto.py generateLog \
    --log=<logfile> \
    --init=<initialSet> \
    --timestamp=<T> \
    --mode=<mode> \
    --model_path=<model_path> \
    --prob=<prob> \
    --dtlog=<dtlog> \
    [--states=<states>]
```

## 3. Check Safety
Evaluate whether logged trajectories satisfy constraints.

```
posto.py checkSafety \
    --log=<logfile> \
    --mode=<mode> \
    --model_path=<model_path> \
    [--states=<states>] \
    [--constraints=<constraints>]
```

## Development Mode
Custom next‑state function without modifying core `Posto` code.

Example:
```python
from System import System

def my_getNextState(state):
    x, y = state
    x_next = x + 0.1 * (y - x)
    y_next = y + 0.1 * (x - y)
    return (x_next, y_next)

sys = System(
    log_path="/path/to/output.lg",
    states=["x", "y"],
    constraints=[(0, "le", 1)]
)

sys.getNextState = my_getNextState

sys.behaviour([[0, 1], [0, 1]], T=100)
sys.generateLog([[0, 1], [0, 1]], T=100, prob=0.5, dtlog=0.1)
sys.checkSafety()
```
Run the above using the command:

```bash
python dev/Model.py
```

Run the above using the command:

```bash
python dev/Model.py
```

## Required Packages

- `numpy`  
- `scipy`  
- `mpmath`  
- `matplotlib`  
- `docopt`  
- `tensorflow`  
- `tqdm`
