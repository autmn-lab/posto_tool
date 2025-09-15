import os,sys,copy
import time
import ast

PROJECT_ROOT = os.environ['MNTR_BB_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *
from lib.GenLog import *
from lib.TrajValidity import *
from lib.TrajSafety import *
from lib.JFBF import *
from lib.Visualize import *
from lib.Equation import *
#from lib.ANN import *



class System:

    prob = None
    dtlog = None


    def __init__(self, log_path, mode, model_path):
        self.log_path = log_path
        if mode=="equation":
            self.model = Equation(model_path)
        #elif mode=="ann":
            #self.model = ANN(model_path)

    def getNextState(self, state):

        nextState = self.model.getNextState(state)
        return nextState
    

    def getTraj(self, initState, T):
        traj=[]
        state=copy.copy(initState)
        for t in range(T):
            traj.append(state)
            nextState=self.getNextState(state)
            state=copy.copy(nextState)
        return traj
    

    def getRandomTrajs(self,initSet,T,K):
        trajs=[]
        for i in range(K):
            x_init_rand=random.uniform(initSet[0][0], initSet[0][1])
            y_init_rand=random.uniform(initSet[1][0], initSet[1][1])
            traj=self.getTraj((x_init_rand,y_init_rand),T)
            trajs.append(traj)
        return trajs


    def getLog(self, initSet,T):
        trajs=self.getRandomTrajs(initSet,T,1)
        
        logger=GenLog(trajs[0])
        log=logger.genLog(System.dtlog, System.prob)

        viz = Visualize(VIZ, msg)
        viz.vizTrajs(trajs,log[0])


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
        print("Total Trajectories Generated: ",totTrajs*100,"; Valid Trajectories: ",len(valTrajs))
        return valTrajs


    def isSafe(self, initSet,T,unsafe,state,op,Bi,ci):
        ts=time.time()
        trajsL=self.getRandomTrajs(initSet,T,1)
        logger=GenLog(trajsL[0])
        logUn=logger.genLog(System.dtlog, System.prob)[0]
        K=JFB(Bi,ci).getNumberOfSamples()
        isSafe=True
        totTrajs=0
        valTrajObj=TrajValidity(logUn)
        valTrajs=[]
        safeTrajs=[]
        unsafeTrajs=[]
        safeTrajObj=TrajSafety([state,op,unsafe])
        (safeSamps,unsafeSamps)=safeTrajObj.getSafeUnsafeLog(logUn)
        if len(unsafeSamps)==0 or False:
            while len(valTrajs)<=K:
                trajs=self.getRandomTrajs(logUn[0][0],T,100)
                totTrajs+=1
                valTrajsIt,inValTrajsIt=valTrajObj.getValTrajs(trajs)
                valTrajs=valTrajs+valTrajsIt
                print(totTrajs*100,len(valTrajs))
                # Check safety of valTrajsIt
                (safeTrajs,unsafeTrajs)=safeTrajObj.getSafeUnsafeTrajs(valTrajsIt)
                if len(unsafeTrajs)>0:
                    isSafe=False
                    break
                ############################

                if len(valTrajs)>=K:
                    break
        else:
            isSafe=False
        
        ts=time.time()-ts
        print("Time Taken: ",ts)
        print("Safety: ",isSafe)
        print("[Trajs] Safe, Unsafe: ",len(safeTrajs),len(unsafeTrajs))
        print("[Log] Safe, Unsafe: ",len(safeSamps),len(unsafeSamps))
        print("Total Trajectories Generated: ",totTrajs*100,"; Valid Trajectories: ",len(valTrajs))
        return (ts,isSafe)
    
        
    def generateLog(self, init_set, T, prob, dtlog):

        System.prob = prob
        System.dtlog = dtlog

        trajsL = self.getRandomTrajs(init_set, T, 1)
        logger = GenLog(trajsL[0])
        logUn=logger.genLog(System.dtlog, System.prob)[0]

        os.makedirs(os.path.dirname(self.log_path) or ".", exist_ok=True)
        with open(self.log_path, "w") as f:
            for box, t in logUn:
                x_lo, x_hi = box[0]
                y_lo, y_hi = box[1]
                f.write(f"t={int(t)}: [[{x_lo:.6f}, {x_hi:.6f}], [{y_lo:.6f}, {y_hi:.6f}]]\n")


    def readLog(self):
        
        logUn = []
        with open(self.log_path, "r") as f:
            for line in f:
                # Each line in the log looks like: t=0: [[x_lo,x_hi],[y_lo,y_hi]]
                t_part, box_part = line.strip().split(":")
                t = int(t_part.split("=")[1])
                # Use ast.literal_eval to safely parse the box lists
                box = ast.literal_eval(box_part.strip())
                logUn.append((box, t))
        return logUn


    def checkSafety( self, T, unsafe, state, op,):

        ts = time.time()
        logUn = self.readLog()

        K = JFB(B, c).getNumberOfSamples()
        isSafe = True
        totTrajs = 0
        valTrajObj = TrajValidity(logUn)
        valTrajs = []
        safeTrajs = []
        unsafeTrajs = []
        safeTrajObj = TrajSafety([state, op, unsafe])

        (safeSamps, unsafeSamps) = safeTrajObj.getSafeUnsafeLog(logUn)

        if len(unsafeSamps) == 0 or False:
            # Generate random trajectories from the lower-left corner of the first box
            while len(valTrajs) <= K:
                trajs = self.getRandomTrajs(logUn[0][0], T, 100)
                totTrajs += 1
                valTrajsIt, inValTrajsIt = valTrajObj.getValTrajs(trajs)
                print(totTrajs * 100, len(valTrajs))
                # Check safety of valTrajsIt
                (safeTrajs, unsafeTrajs) = safeTrajObj.getSafeUnsafeTrajs(valTrajsIt)
                if len(unsafeTrajs) > 0:
                    isSafe = False
                    break
                # accumulate valid trajectories
                valTrajs = valTrajs + valTrajsIt
                if len(valTrajs) >= K:
                    break
        else:
            isSafe = False

        ts = time.time() - ts
        print("Time Taken: ", ts)
        print("Safety: ", isSafe)
        print("[Trajs] Safe, Unsafe: ", len(safeTrajs), len(unsafeTrajs))
        print("[Log] Safe, Unsafe: ", len(safeSamps), len(unsafeSamps))
        print("Total Trajectories Generated: ", totTrajs * 100, "; Valid Trajectories: ", len(valTrajs))

        # Plotting logic remains unchanged
        sv = False
        viz = Visualize(VIZ, msg)
        if len(unsafeSamps) > 0:
            viz.vizLogsSafeUnsafe2D(T, safeSamps, unsafeSamps, unsafe, state, save=sv, name="JetSafeUnsafeLogs")
        if len(unsafeTrajs) > 0 and len(safeTrajs) > 0:
            viz.vizTrajsSafeUnsafe2D([safeTrajs[0]], [unsafeTrajs[0]], safeSamps, unsafeSamps,
                                    unsafe, state, save=sv, name="JetSafeUnsafeTrajs")
        elif len(safeTrajs) > 0 and len(unsafeTrajs) == 0:
            viz.vizTrajsVal2D(safeTrajs, logUn, unsafe, state, save=sv, name="JetSafeTrajs")
        elif len(unsafeTrajs) > 0:
            viz.vizTrajsVal2D(unsafeTrajs, logUn, unsafe, state, save=True, name="JetUnsafeTrajs")

