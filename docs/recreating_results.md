## Artifact Evaluation

This section outlines the steps to recreate the plots presented in the paper. It is worth noting that the safety verification method proposed in our work is inherently _statistical_. Consequently, the reproduction of the plots will not yield an exact match but rather a _stochastic recreation_. In other words, the plots are recreated using the same set of parameters as in the draft, which define the distributions. The recreated plots represent one possible outcome from that distribution, hence the term "stochastic recreation". As a result, some figures that were initially inferred to be safe in the draft may yield unsafe results (or vice versa) during this process.

It is important to note that this does not affect the soundness of our method. Rather, it reaffirms the stochastic nature of our work, and such stochastic recreations demonstrate the influence of various parameters on the proposed method, as explored in the research questions of the paper. In simpler terms, while the recreated plots may not be identical (in a deterministic sense), they are stochastically equivalent.

To elaborate on the sources of stochasticity, the following factors contribute to the variability in the generated plots (testing this by running the scripts multiple times could be a good approach):

1. Although the same parameters (logging probability and log noise) are used to generate the logs, the logs themselves are _random_, though stochastically equivalent, as they are derived from the same distribution.
2. Additionally, the safety verification process is inherently stochastic, meaning that safety inferences could vary across different iterations. 

### Recreating Figures

1. **To recreate figs. A.2(a)-(c), A.3(a)-(d), A.4(a)-(d) and B.5 perform the following steps:**

   1. Make sure you are in location `/path/to/Posto`

      * ```bash
        cd /path/to/Posto
        ```

   2. Run the following command if the location is not added to the `~/.bashrc`

      * ```bash
        export POSTO_ROOT_DIR=/path/to/Posto
        ```

   3. Run the `artEval.py` with the figure number as the argument to recreate the desired figure

      * ```bash
        python artEval.py --fig=A2a 
        ```

        ![3(a)](https://github.com/bineet-coderep/monitor-bb/blob/main/figs/3(a).png)

      * ```bash
        python artEval.py --fig=A2b 
        ```

        ![3(b)](https://github.com/bineet-coderep/monitor-bb/blob/main/figs/3(b).png)

      * ```bash
        python artEval.py --fig=A2c 
        ```

        ![3(c)](https://github.com/bineet-coderep/monitor-bb/blob/main/figs/3(c).png) 

      * ```bash
        #Choose from A3a, A3b, A3c, A3d
        python artEval.py --fig=A3a 
        ```

        ![Fig4](https://github.com/bineet-coderep/monitor-bb/blob/main/figs/Fig4.png)

      * ```bash
        #Choose from A4a, A4b, A4c, A4d
        python artEval.py --fig=A4a 
        ```

        **NOTE:** This will generate the image showing the plot for the other variable first, followed by fig. A.4(a). Be sure to close the figure window to view the next figure. This is similar for all figures A.4(a)-(d).

        ![Fig4](https://github.com/bineet-coderep/monitor-bb/blob/main/figs/Fig5.png)

      * ```bash
        python artEval.py --fig=B5 
        ```

        
