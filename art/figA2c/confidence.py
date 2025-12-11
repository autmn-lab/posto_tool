import os,sys

PROJECT_ROOT = os.environ['POSTO_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

import time
from Parameters import *
from System import System
from lib.GenLog import GenLog
from lib.TrajValidity import TrajValidity
from lib.TrajSafety import TrajSafety
from lib.JFBF import JFB
import matplotlib.pyplot as plt

class confidence:
    def __init__(self, System):

        self.Bi = B
        self.initSet=[[0.8,1],[0.8,1]]
        self.T=2000
        self.Jet = System

    def varyC(self):
        cList=[0.6,0.7,0.8,0.9,0.99]
        tList=[]
        sList=[]
        for ci in cList:
            print(">> c = ",ci)
            (t,sF)=self.isSafe(ci)
            tList.append(t)
            sList.append(sF)
            print("=====================\n\n")

        print(tList)
        print(sList)
        self.vizVaryC(cList,sList,tList,True,"JetVaryC")

    def vizVaryC(self,cList,sList,tList,save=False,name="Untitled"):
        plt.xlabel(r'$c$',fontsize=20,fontweight = 'bold')
        plt.ylabel(r'Time taken',fontsize=20,fontweight = 'bold')
        L=len(cList)
        
        plt.plot(cList,tList,linewidth=5,linestyle='dashed')

        for i in range(L):
            if sList[i]==True:
                plt.scatter(cList[i], tList[i], s=350, c='green')
            else:
                plt.scatter(cList[i], tList[i], s=350, c='red')
        
        if save:
            out = os.path.join('art/figA2c', f"{name}.pdf")
            plt.savefig(out, format="pdf", bbox_inches="tight")
        
        plt.show()
        plt.clf()

    
    def isSafe(self, ci):
        ts=time.time()
        trajsL=self.Jet.getRandomTrajs(self.initSet,self.T,1)
        logger=GenLog(trajsL[0])
        logUn=logger.genLog(0.02, 5)[0]
        K=JFB(self.Bi,ci).getNumberOfSamples()
        isSafe=True
        totTrajs=0
        valTrajObj=TrajValidity(logUn)
        valTrajs=[]
        safeTrajs=[]
        unsafeTrajs=[]
        safeTrajObj=TrajSafety(self.Jet.constraints)
        (safeSamps,unsafeSamps)=safeTrajObj.getSafeUnsafeLog(logUn)
        if len(unsafeSamps)==0 or False:
            while len(valTrajs)<=K:
                trajs=self.Jet.getRandomTrajs(logUn[0][0],self.T,100)
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
        
        return (ts,isSafe)

