import os,sys,copy
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import time
import ast
import json

PROJECT_ROOT = os.environ['MNTR_BB_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *
from lib.GenLog import *
from lib.TrajValidity import *
from lib.TrajSafety import *
from lib.JFBF import *
from lib.Visualize import *
from lib.Equation import *
from lib.ANN import *
from concurrent.futures import ProcessPoolExecutor

random.seed(42)

class System:

    prob = None
    dtlog = None


    def __init__(self, log_path, mode=None, model_path=None, states=None, constraints=None):

        self.log_path   = log_path
        self.mode       = mode
        self.model_path = model_path

        # Select model
        if mode == "equation":
            self.model = Equation(model_path)
        elif mode == "ann":
            self.model = ANN(model_path)

        self.imgdir = os.path.join(os.path.dirname(self.log_path), "img")

        # -------------------------
        # Shortened constraint logic
        # -------------------------
        self.constraints = constraints
        self.state_names = states

        # Helper to parse a JSON constraints/model file
        def load_spec(path):
            with open(path, "r") as f:
                spec = json.load(f)
            state_vars = spec.get("state_vars", [])
            cons_list  = spec.get("safety_constraints", [])
            processed  = []

            for item in cons_list:
                if isinstance(item, dict):
                    st  = item.get("state_idx", item.get("state"))
                    op  = item.get("op",        item.get("inequal"))
                    val = item.get("const",     item.get("value"))
                else:
                    st, op, val = item

                if isinstance(st, str):
                    st = state_vars.index(st)
                if val is None:
                    raise ValueError(f"Constraint {item!r} missing numeric constant")
                processed.append((int(st), op, float(val)))

            return state_vars, processed

    
        if isinstance(constraints, str) and constraints.endswith(".json"):
            self.state_names, self.constraints = load_spec(constraints)
            return

    
        if mode == "equation" and model_path:
            self.state_names, self.constraints = load_spec(model_path)
            return

        if constraints is not None and model_path is None:
            if self.state_names is None:
                raise ValueError("states cannot be None when no JSON constraints and no model_path")



    def getNextState(self, state):
        nextState = self.model.getNextState(state)
        return nextState

    def getTraj(self, initState, T):
        traj=[]
        state=copy.copy(initState)
        for t in range(T):
            traj.append(state)
            nextState=self.getNextState(state)
            if nextState is None:
                print(f"{msg.WARNING}[WARN]{msg.ENDC} Overflow encountered — using current state as final and stopping.")
                # Overflow detected; stop processing
                break
            state=copy.copy(nextState)
        return traj
    

    def getRandomTrajs(self,initSet,T,K):
        trajs=[]
        for i in range(K):
            point = []                           
            for dim in initSet:                 
                value = random.uniform(dim[0], dim[1])   
                point.append(value)          
            traj = self.getTraj(tuple(point), T) 
            trajs.append(traj)                   
        return trajs   


    def getValidTrajs(self,initSet,T,K,logUn):
        totTrajs=0
        valTrajObj=TrajValidity(logUn)
        valTrajs=[]
        while len(valTrajs)<=K:
            trajs=self.getRandomTrajs(logUn[0][0],T,100)
            totTrajs+=1
            valTrajsIt,inValTrajsIt=valTrajObj.getValTrajs(trajs)
            valTrajs=valTrajs+valTrajsIt
            if len(valTrajs)>=K:
                break
        print(f"{msg.HEADER}Total Trajectories Generated:{msg.ENDC} "
                f"{msg.BOLD}{totTrajs * 100}{msg.ENDC} ; "
                f"{msg.OKCYAN}Valid Trajectories:{msg.ENDC} "
                f"{msg.BOLD}{len(valTrajs)}{msg.ENDC}")
        return valTrajs

    
    def behaviour(self, init_set, T):
        start = time.time()

        info("Starting behavior generation...")
        note(f"Initial set: {init_set}")
        note(f"Time horizon: {T}")
        note(f"Mode: {self.mode}")
        note(f"Model file: {self.model_path}")
        
        if self.mode=='ann':
            trajs = self.behaveANN(init_set, T)
        else:
            trajs = self.behave(init_set, T)

        prefix = "behaviorPair"
        nStates = len(trajs[0][0])
        for (i, j) in combinations(range(nStates), 2):
            pair_trajs = []
            for traj in trajs:
                new_traj = [ [point[i], point[j]] for point in traj ]
                pair_trajs.append(new_traj)
            viz = Visualize(VIZ, msg, self.imgdir, self.state_names)
            viz.vizTrajs(i, j, pair_trajs, logUn=None, save=True,
                        name=f"{prefix}_{i}_{j}")

        ok("Behavior generated successfully.")
        ok(f"Stored at: {msg.UNDERLINE}{self.imgdir}{msg.ENDC}")
        elapsed = time.time() - start
        print(f"{msg.HEADER}[INFO]{msg.ENDC} Time taken: {msg.BOLD}{elapsed:.4f} sec{msg.ENDC}")

    def behave(self, init_set, T):

        trajs = self.getRandomTrajs(init_set, T, 1)
        return trajs
            
    def behaveANN(self, init_set, T):
        K=1
        n_states = len(init_set)
        states = []
        for i in range(K):
            point = []
            for dim in init_set:
                point.append(random.uniform(dim[0], dim[1]))
            states.append(point)

       
        trajs = [[] for _ in range(K)]
        ann_model = self.model

        for t in range(T):
            
            for idx in range(K):
                trajs[idx].append(tuple(states[idx]))

            try:
                single_tensors = [ann_model.prepareInput(s) for s in states]
                x_batch = np.concatenate(single_tensors, axis=0)

                #check if predictions are in order
                out = ann_model.model.predict(x_batch, verbose=0)
                out_flat = out.reshape((K, -1))
                states = [list(map(float, out_flat[i])) for i in range(K)]
            except Exception:
                new_states = []
                for s in states:
                    ns = ann_model.getNextState(s)
                    new_states.append(list(ns))
                states = new_states

        return trajs

        

        
    def generateLog(self, init_set, T, prob, dtlog):

        start = time.time()

        info("Starting log generation...")
        note(f"Initial set: {init_set}")
        note(f"Time horizon: {T}")
        note(f"Mode: {self.mode}")
        note(f"Model file: {self.model_path}")
        note(f"Logging probability: {prob}")
        note(f"Delta log: {dtlog}")
        note(f"Output log path: {self.log_path}")
     
        System.prob = prob
        System.dtlog = dtlog

        trajsL = self.getRandomTrajs(init_set, T, 1)
        logger = GenLog(trajsL[0])
        logUn=logger.genLog(System.dtlog, System.prob)[0]

        os.makedirs(os.path.dirname(self.log_path) or ".", exist_ok=True)
        with open(self.log_path, "w") as f:
            for box, t in logUn:
                interval_strs = []
                for (lo, hi) in box:
                    interval_strs.append(f"[{lo}, {hi}]")
                intervals_line = ", ".join(interval_strs)
                f.write(f"t={int(t)}: [{intervals_line}]\n")

        viz = Visualize(VIZ, msg, self.imgdir, self.state_names)
        viz.vizLog(logUn, save=True)
        viz.vizTrajLog(trajsL, logUn, save=True, name_prefix="traj_log_pair")


        ok("Log generated successfully.")
        ok(f"Stored at: {msg.UNDERLINE}{self.log_path}{msg.ENDC}")
        elapsed = time.time() - start
        print(f"{msg.HEADER}[INFO]{msg.ENDC} Time taken: {msg.BOLD}{elapsed:.4f} sec{msg.ENDC}")
        


    def readLog(self):  
        logUn = []
        max_t = 0
        with open(self.log_path, "r") as f:
            for line in f:
                # Each line in the log looks like: t=0: [[x_lo,x_hi],[y_lo,y_hi]]
                t_part, box_part = line.strip().split(":")
                t = int(t_part.split("=")[1])
                # Use ast.literal_eval to safely parse the box lists
                box = ast.literal_eval(box_part.strip())
                logUn.append((box, t))
                if t > max_t:
                    max_t = t
        return logUn, max_t


    def checkSafety(self):
        info("Running safety check...")
        note(f"Log path: {self.log_path}")
        note(f"Mode: {self.mode}")
        note(f"Model File: {self.model_path}")

        # Ensure constraints have been loaded
        if not self.constraints:
            raise RuntimeError("No constraints defined in the model; cannot perform safety check.")

        # Create the safety checker with all constraints
        safety_checker = TrajSafety(self.constraints)
        note("Using constraints from JSON model:")
        for st_idx, oper, bound in self.constraints:
            note(f"  state[{st_idx}] {oper} {bound}")

        ts_start = time.time()
        logUn, T = self.readLog()
        T = T + 1
        K = JFB(B, c).getNumberOfSamples()
        isSafe = True
        totTrajs = 0
        valTrajObj = TrajValidity(logUn)
        valTrajs = []
        safeTrajs = []
        unsafeTrajs = []

        # Check the log samples for immediate violations
        safeSamps, unsafeSamps = safety_checker.getSafeUnsafeLog(logUn)

        if len(unsafeSamps) == 0:
            # Generate and test random trajectories
            while len(valTrajs) <= K:
                try:
                    # Generate K valid trajectories from the initial log box
                    trajs = self.getRandomTrajs(logUn[0][0], T, 100)
                except OverflowError as e:
                    print(f"{msg.FAIL}[ERROR]{msg.ENDC} {e}")
                    print(f"{msg.WARNING}[HINT]{msg.ENDC} Aborting safety check because the system state blew up.")
                    return
                totTrajs += 1
                valTrajsIt, inValTrajsIt = valTrajObj.getValTrajs(trajs)
                print(f"{msg.HEADER}Total Trajectories Generated:{msg.ENDC} "
                    f"{msg.BOLD}{totTrajs * 100}{msg.ENDC} ; "
                    f"{msg.OKCYAN}Valid Trajectories:{msg.ENDC} "
                    f"{msg.BOLD}{len(valTrajs)}{msg.ENDC}")
                safe_it, unsafe_it = safety_checker.getSafeUnsafeTrajs(valTrajsIt)
                safeTrajs += safe_it
                unsafeTrajs += unsafe_it
                if unsafe_it:
                    isSafe = False
                    break
                valTrajs += valTrajsIt
                if len(valTrajs) >= K:
                    break
        else:
            isSafe = False

        ts = time.time() - ts_start
        print(f"{msg.BOLD}Time Taken:{msg.ENDC} {msg.OKCYAN}{ts}{msg.ENDC}")

        # Reporting results
        if isSafe:
            print(f"{msg.BOLD}Safety:{msg.ENDC} {msg.OKGREEN}{msg.BOLD}SAFE{msg.ENDC}")
        else:
            print(f"{msg.BOLD}Safety:{msg.ENDC} {msg.FAIL}{msg.BOLD}UNSAFE{msg.ENDC}")
        print(f"{msg.OKBLUE}[Trajs]{msg.ENDC} {msg.OKGREEN}Safe:{msg.ENDC} {len(safeTrajs)} "
            f"{msg.FAIL}Unsafe:{msg.ENDC} {len(unsafeTrajs)}")
        print(f"{msg.OKCYAN}[Log]{msg.ENDC} {msg.OKGREEN}Safe:{msg.ENDC} {len(safeSamps)} "
            f"{msg.FAIL}Unsafe:{msg.ENDC} {len(unsafeSamps)}")
        print(f"{msg.HEADER}Total Trajectories Generated:{msg.ENDC} {msg.BOLD}{totTrajs * 100}{msg.ENDC} ; "
            f"{msg.OKCYAN}Valid Trajectories:{msg.ENDC} {msg.BOLD}{len(valTrajs)}{msg.ENDC}")

        viz = Visualize(VIZ, msg, self.imgdir, self.state_names)

        n_states = len(logUn[0][0]) if logUn else 0

        for state_idx in range(n_states):
            bounds = [const for (st, op, const) in self.constraints if st == state_idx]

            if unsafeSamps:
                viz.vizLogsSafeUnsafe2D(
                    T, safeSamps, unsafeSamps,
                    bounds, state_idx, save=True,
                    name=f"SafeUnsafeLogs_state{state_idx}"
                )

            if unsafeTrajs and safeTrajs:
                viz.vizTrajsSafeUnsafe2D(
                    [safeTrajs[0]], [unsafeTrajs[0]],
                    safeSamps, unsafeSamps,
                    bounds, state_idx, save=True,
                    name=f"SafeUnsafeTrajs_state{state_idx}"
                )
            elif safeTrajs and not unsafeTrajs:
                viz.vizTrajsVal2D(
                    safeTrajs, logUn, bounds,
                    state_idx, save=True,
                    name=f"SafeTrajs_state{state_idx}"
                )
                viz.vizTrajsSafeUnsafe2D(
                    [safeTrajs[0]], None,
                    safeSamps, None,
                    bounds, state_idx, save=True,
                    name=f"SafeUnsafeTrajs_state{state_idx}"
                )
            elif unsafeTrajs:
                viz.vizTrajsVal2D(
                    unsafeTrajs, logUn, bounds,
                    state_idx, save=True,
                    name=f"UnsafeTrajs_state{state_idx}"
                )
