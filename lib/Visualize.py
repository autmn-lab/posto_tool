import os,sys,copy

PROJECT_ROOT = os.environ['MNTR_BB_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

import random
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d

class Visualize:

    def __init__(self, viz, msg):
        self.viz = viz
        self.msg = msg

    def vizTrajs(self, trajs,logUn=None,save=False,name="Untitled"):

        if self.viz == False:
            print(f"{self.msg.WARNING}[WARN]{self.msg.ENDC} Graphical visualization disabled. "
            f"Set {self.msg.BOLD}VIZ=True{self.msg.ENDC} to enable.")
            return

        ax = plt.axes(projection='3d')
        ax.set_xlabel('x',fontsize=20,fontweight='bold')
        ax.set_ylabel('y',fontsize=20,fontweight='bold')
        ax.set_zlabel('time',fontsize=8,fontweight='bold')

        if logUn!=None:
            for lg in logUn:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.Rectangle((lg[0][0][0], lg[0][1][0]), wd, ht, facecolor='none', edgecolor='black',linewidth=0.4,alpha=0.5)
                ax.add_patch(p)
                art3d.pathpatch_2d_to_3d(p, z=lg[1], zdir="z")

        for traj in trajs:
            x=[p[0] for p in traj]
            y=[p[1] for p in traj]
            t=list(range(0,len(traj)))
            ax.plot3D(x, y, t)

        if save:
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()
        
    def vizTrajsVal(self, trajsVal,trajsInVal,logUn=None,save=False,name="Untitled"):

        if self.viz == False:
            print(f"{self.msg.WARNING}[WARN]{self.msg.ENDC} Graphical visualization disabled. "
            f"Set {self.msg.BOLD}VIZ=True{self.msg.ENDC} to enable.")
            return

        ax = plt.axes(projection='3d')
        ax.set_xlabel('x',fontsize=20,fontweight='bold')
        ax.set_ylabel('y',fontsize=20,fontweight='bold')
        ax.set_zlabel('time',fontsize=8,fontweight='bold')

        if logUn!=None:
            for lg in logUn:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.Rectangle((lg[0][0][0], lg[0][1][0]), wd, ht, facecolor='none', edgecolor='black',linewidth=0.4,alpha=0.5)
                ax.add_patch(p)
                art3d.pathpatch_2d_to_3d(p, z=lg[1], zdir="z")

        for traj in trajsVal:
            x=[p[0] for p in traj]
            y=[p[1] for p in traj]
            t=list(range(0,len(traj)))
            ax.plot3D(x, y, t,color='blue')

        for traj in trajsInVal:
            x=[p[0] for p in traj]
            y=[p[1] for p in traj]
            t=list(range(0,len(traj)))
            ax.plot3D(x, y, t,color='red',alpha=0.3)
    
        if save:
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()

    def vizTrajsVal2D(self, trajsVal,logUn=None,unsafe=0.0,state=0,save=False,name="Untitled"):

        if self.viz == False:
            print(f"{self.msg.WARNING}[WARN]{self.msg.ENDC} Graphical visualization disabled. "
            f"Set {self.msg.BOLD}VIZ=True{self.msg.ENDC} to enable.")
            return

        lnWd=2

        t=list(range(len(trajsVal[0])))

        plt.xlabel("Time",fontsize=20,fontweight='bold')
        plt.ylabel("State-"+str(state),fontsize=20,fontweight='bold')

        for traj in trajsVal:
            x=[p[state] for p in traj]
            plt.plot(t,x,linewidth=lnWd)

        if logUn!=None:
            for lg in logUn:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.plot([lg[1],lg[1]],[lg[0][state][0], lg[0][state][1]], color='black',linewidth=lnWd,alpha=0.6)

        if unsafe!=None:
            p = plt.plot(t, [unsafe]*len(t),color='red',linewidth=lnWd,linestyle='dashed')

        if save:
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()

    def vizTrajsValInVal2D(self, trajsVal,inValTrajs,logUn=None,unsafe=None,state=0,save=False,name="Untitled"):

        if self.viz == False:
            print(f"{self.msg.WARNING}[WARN]{self.msg.ENDC} Graphical visualization disabled. "
            f"Set {self.msg.BOLD}VIZ=True{self.msg.ENDC} to enable.")
            return

        lnWd=2

        t=list(range(len(trajsVal[0])))

        plt.xlabel("Time",fontsize=20,fontweight='bold')
        plt.ylabel("State-"+str(state),fontsize=20,fontweight='bold')

        for traj in trajsVal:
            x=[p[state] for p in traj]
            plt.plot(t,x,linewidth=lnWd,color='blue')

        for traj in inValTrajs:
            x=[p[state] for p in traj]
            plt.plot(t,x,linewidth=lnWd,color='magenta')

        if logUn!=None:
            for lg in logUn:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.plot([lg[1],lg[1]],[lg[0][state][0], lg[0][state][1]], color='black',linewidth=lnWd)

        if unsafe!=None:
            p = plt.plot(t, [unsafe]*len(t),color='red',linewidth=lnWd,linestyle='dashed')

        if save:
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()

    def vizTrajsSafeUnsafe2D(self, safeTrajs, unsafeTrajs, safeSamps, unsafeSamps, unsafe=0.0, state=0, save=False, name="Untitled"):

        if self.viz == False:
            print(f"{self.msg.WARNING}[WARN]{self.msg.ENDC} Graphical visualization disabled. "
            f"Set {self.msg.BOLD}VIZ=True{self.msg.ENDC} to enable.")
            return

        lnWd=2

        if len(safeTrajs)>0:
            t=list(range(len(safeTrajs[0])))
        else:
            t=list(range(len(unsafeTrajs[0])))

        plt.xlabel("Time",fontsize=20,fontweight='bold')
        plt.ylabel("State-"+str(state),fontsize=20,fontweight='bold')

        for traj in safeTrajs:
            x=[p[state] for p in traj]
            plt.plot(t,x,linewidth=lnWd,color='blue')
        
        for traj in unsafeTrajs:
            x=[p[state] for p in traj]
            plt.plot(t,x,linewidth=lnWd,color='red',linestyle='dashdot',alpha=0.8)

        if safeSamps!=None:
            for lg in safeSamps:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.plot([lg[1],lg[1]],[lg[0][state][0], lg[0][state][1]], color='black',linewidth=lnWd)
        
        if unsafeSamps!=None:
            for lg in unsafeSamps:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.plot([lg[1],lg[1]],[lg[0][state][0], lg[0][state][1]], color='brown',linewidth=lnWd)

        p = plt.plot(t, [unsafe]*len(t),color='red',linewidth=lnWd,linestyle='dashed')

        if save:
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()

    def vizLogsSafeUnsafe2D(self, T, safeSamps, unsafeSamps, unsafe=0.0, state=0, save=False, name="Untitled"):

        if self.viz == False:
            print(f"{self.msg.WARNING}[WARN]{self.msg.ENDC} Graphical visualization disabled. "
            f"Set {self.msg.BOLD}VIZ=True{self.msg.ENDC} to enable.")
            return

        lnWd=2

        t=list(range(T))

        plt.xlabel("Time",fontsize=20,fontweight='bold')
        plt.ylabel("State-"+str(state),fontsize=20,fontweight='bold')

        if safeSamps!=None:
            for lg in safeSamps:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.plot([lg[1],lg[1]],[lg[0][state][0], lg[0][state][1]], color='black',linewidth=lnWd)
        
        if unsafeSamps!=None:
            for lg in unsafeSamps:
                wd=abs(lg[0][0][1]-lg[0][0][0])
                ht=abs(lg[0][1][1]-lg[0][1][0])
                p = plt.plot([lg[1],lg[1]],[lg[0][state][0], lg[0][state][1]], color='brown',linewidth=lnWd)

        p = plt.plot(t, [unsafe]*len(t),color='red',linewidth=lnWd,linestyle='dashed')

        if save:
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()

    def vizVaryC(self, cList, sList, tList, save=False, name="Untitled"):

        if self.viz == False:
            print(f"{self.msg.WARNING}[WARN]{self.msg.ENDC} Graphical visualization disabled. "
            f"Set {self.msg.BOLD}VIZ=True{self.msg.ENDC} to enable.")
            return

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
            plt.savefig(name+".pdf", format="pdf", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()