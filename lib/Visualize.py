import os,sys,copy

PROJECT_ROOT = os.environ['MNTR_BB_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

import random
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
from itertools import combinations


class Visualize:

    def __init__(self, viz, msg, path):
        self.viz = viz
        self.msg = msg
        self.path = path

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
            out = os.path.join(self.path, f"{name}.png")
            plt.savefig(out, format="png", bbox_inches="tight")
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
            out = os.path.join(self.path, f"{name}.png")
            plt.savefig(out, format="png", bbox_inches="tight")
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
            out = os.path.join(self.path, f"{name}.png")
            plt.savefig(out, format="png", bbox_inches="tight")
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
            out = os.path.join(self.path, f"{name}.png")
            plt.savefig(out, format="png", bbox_inches="tight")
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
            out = os.path.join(self.path, f"{name}.png")
            plt.savefig(out, format="png", bbox_inches="tight")
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
            out = os.path.join(self.path, f"{name}.png")
            plt.savefig(out, format="png", bbox_inches="tight")
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
            out = os.path.join(self.path, f"{name}.png")
            plt.savefig(out, format="png", bbox_inches="tight")
        else:
            plt.show()
        plt.clf()


    def statePairs(self, nStates):
        return list(combinations(range(nStates), 2))


    def vizLog(self, logUn, save=False):

        if not self.viz:
            print(f"{self.msg.WARNING}[WARN]{self.msg.ENDC} Graphical visualization disabled. "
                  f"Set {self.msg.BOLD}VIZ=True{self.msg.ENDC} to enable.")
            return

        if not logUn:
            print(f"{self.msg.WARNING}[WARN]{self.msg.ENDC} Empty log; nothing to plot.")
            return

        # Infer number of states from the first entry: lg[0] -> list of intervals
        try:
            nStates = len(logUn[0][0])
        except Exception:
            print(f"{self.msg.FAIL}[ERR]{self.msg.ENDC} logUn format not recognized.")
            return

        pairs = self.statePairs(nStates)

        # Compute global axis ranges for better scaling
        mins = [float('inf')] * nStates
        maxs = [-float('inf')] * nStates
        times = []

        for lg in logUn:
            print(lg)
            print(lg[0])
            intervals, t = lg[0], lg[1]
            times.append(t)
            for s_idx in range(nStates):
                lo, hi = intervals[s_idx]
                if lo < mins[s_idx]: mins[s_idx] = lo
                if hi > maxs[s_idx]: maxs[s_idx] = hi

        t_min = min(times)
        t_max = max(times) if times else 1.0

        for (i, j) in pairs:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.set_xlabel(f'state {i}', fontsize=12, fontweight='bold')
            ax.set_ylabel(f'state {j}', fontsize=12, fontweight='bold')
            ax.set_zlabel('time', fontsize=10, fontweight='bold')
            ax.set_title(f'Log Boxes: state {i} vs state {j} vs time', fontsize=12)

            # axis limits
            ax.set_xlim(mins[i], maxs[i])
            ax.set_ylim(mins[j], maxs[j])
            ax.set_zlim(t_min, t_max)

            # draw each rectangle at its time z = t
            for lg in logUn:
                intervals, t = lg[0], lg[1]
                lo_i, hi_i = intervals[i]
                lo_j, hi_j = intervals[j]
                width = hi_i - lo_i
                height = hi_j - lo_j
                if width <= 0 or height <= 0:
                    continue

                rect = plt.Rectangle((lo_i, lo_j), width, height,
                                     facecolor='brown', edgecolor='brown', alpha=0.8, linewidth=0.6)
                ax.add_patch(rect)
                art3d.pathpatch_2d_to_3d(rect, z=t, zdir="z")

            if save:
                out = os.path.join(self.path, f"pair_{i}_{j}.png")
                plt.savefig(out, format="png", bbox_inches="tight")
            else:
                plt.show()

            plt.clf()
            plt.close(fig)


    def vizTrajLog(self, trajs, logUn, save=False, name_prefix="traj_log_pair"):
        
        if not self.viz:
            print(f"{self.msg.WARNING}[WARN]{self.msg.ENDC} Graphical visualization disabled. "
                f"Set {self.msg.BOLD}VIZ=True{self.msg.ENDC} to enable.")
            return
        if not trajs:
            print(f"{self.msg.WARNING}[WARN]{self.msg.ENDC} No trajectories provided.")
            return

        # Determine state dimensionality
        nStates = len(trajs[0][0])
        if nStates < 2:
            print(f"{self.msg.WARNING}[WARN]{self.msg.ENDC} Need at least 2 state variables to plot pairs.")
            return

        # Precompute axis limits across boxes and trajectories
        mins = [float('inf')] * nStates
        maxs = [-float('inf')] * nStates
        times = []
        if logUn:
            for intervals, t in logUn:
                times.append(t)
                for s_idx, (lo, hi) in enumerate(intervals):
                    if lo < mins[s_idx]: mins[s_idx] = lo
                    if hi > maxs[s_idx]: maxs[s_idx] = hi
        # Include trajectory data in axis limits
        for traj in trajs:
            for st in traj:
                for s_idx, val in enumerate(st):
                    if val < mins[s_idx]: mins[s_idx] = val
                    if val > maxs[s_idx]: maxs[s_idx] = val
        t_min = min(times) if times else 0
        t_max = max(times) if times else max(len(traj) for traj in trajs) - 1

        pairs = self.statePairs(nStates)
        for (i, j) in pairs:
            fig = plt.figure(figsize=(12, 5))
            ax = fig.add_subplot(111, projection='3d')
            ax.set_xlabel(f'state {i}', fontsize=12, fontweight='bold')
            ax.set_ylabel(f'state {j}', fontsize=12, fontweight='bold')
            ax.set_zlabel('time', fontsize=10, fontweight='bold')
            ax.set_xlim(mins[i], maxs[i])
            ax.set_ylim(mins[j], maxs[j])
            ax.set_zlim(t_min, t_max)

            # Draw uncertainty rectangles from the log
            if logUn:
                for intervals, t in logUn:
                    lo_i, hi_i = intervals[i]
                    lo_j, hi_j = intervals[j]
                    width = hi_i - lo_i
                    height = hi_j - lo_j
                    if width <= 0 or height <= 0:
                        continue
                    rect = plt.Rectangle(
                        (lo_i, lo_j), width, height,
                        facecolor='brown', edgecolor='brown',
                        alpha=0.8, linewidth=0.6
                    )
                    ax.add_patch(rect)
                    art3d.pathpatch_2d_to_3d(rect, z=t, zdir="z")

            # Plot each trajectory as a 3D line
            for traj in trajs:
                xs = [st[i] for st in traj]
                ys = [st[j] for st in traj]
                zs = list(range(len(traj)))
                ax.plot(xs, ys, zs, linewidth=1.5, color='blue')

            if save:
                plt.tight_layout()
                out = os.path.join(self.path, f"{name_prefix}_{i}_{j}.png")
                plt.savefig(out, format="png", bbox_inches="tight")
            else:
                plt.tight_layout()
                plt.show()
            plt.clf()
            plt.close(fig)
