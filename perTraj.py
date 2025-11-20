from System import *

states = ['x', 'y', 'z']

sys1 = System("logs/modeltest.lg", 'equation', '/home/prachi-bhattacharjee/Posto/models/modelDNN.json' )
sys2 = System("logs/modeltest.lg", 'ann', '/home/prachi-bhattacharjee/DNN_test/MyModel3.h5')

initState = [[0.1, 0.2], [0.1, 0.2], [0.1, 0.2]]
timeHorizon = 200

def vizTrajs(states, trajs, save=False, name="Untitled"):


    trajs1, trajs2 = trajs   # unpack the two groups

    ax = plt.axes(projection='3d')
    ax.set_xlabel(states[0], fontsize=20, fontweight='bold')
    ax.set_ylabel(states[1], fontsize=20, fontweight='bold')
    ax.set_zlabel('time', fontsize=8, fontweight='bold')

    # Generate distinct colors for each pair
    colors = plt.cm.tab10(np.linspace(0, 1, len(trajs1)))

    for idx, (t1, t2) in enumerate(zip(trajs1, trajs2)):
        c = colors[idx]

        # --- traj1: solid ---
        x1 = [p[0] for p in t1]
        y1 = [p[1] for p in t1]
        tt1 = list(range(len(t1)))

        ax.plot3D(
            x1, y1, tt1,
            color=c,
            linestyle='-',
            linewidth=1.8,
            label=f"Equation" if idx == 0 else ""
        )

        # --- traj2: dotted ---
        x2 = [p[0] for p in t2]
        y2 = [p[1] for p in t2]
        tt2 = list(range(len(t2)))

        ax.plot3D(
            x2, y2, tt2,
            color=c,
            linestyle='--',
            linewidth=1.8,
            label=f"ANN" if idx == 0 else ""
        )

    ax.legend()

   
    out = os.path.join('/home/prachi-bhattacharjee/Posto/logs', f"{name}.png")
    plt.savefig(out, format="png", bbox_inches="tight")

    plt.show()

    plt.clf()



def behave(init_set, T):

    trajs = sys1.getRandomTrajs(init_set, T, 5)
    return trajs
            
def behaveANN(init_set, T,):
    K=5
    n_states = len(init_set)
    states = []
    for i in range(K):
        point = []
        for dim in init_set:
            point.append(random.uniform(dim[0], dim[1]))
        states.append(point)
   
    trajs = [[] for _ in range(K)]
    ann_model = sys2.model

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


sys1.behaviour = behave
sys2.behaviour = behaveANN

traj1 = sys1.behaviour(initState, timeHorizon)
traj2 = sys2.behaviour(initState, timeHorizon)

prefix = "behaviorPair" 

nStates = len(traj1[0][0])  

for (i, j) in combinations(range(nStates), 2): 
    pair_trajs1 = [] 
    pair_trajs2 = [] 
    for traj in traj1: 
        new_traj = [ [point[i], point[j]] for point in traj ] 
        pair_trajs1.append(new_traj) 
    for traj in traj2: 
        new_traj = [ [point[i], point[j]] for point in traj ] 
        pair_trajs2.append(new_traj) 
    viz = vizTrajs(states, [pair_trajs1, pair_trajs2], save=True, name=f"{prefix}_{i}_{j}")
