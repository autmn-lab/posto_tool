#!/usr/bin/env python3
"""
Usage:
    artEval.py --fig=<figno>

"""

from docopt import docopt
import ast
import os
import re
import sys

from System import System
from art.figA2c.confidence import confidence
from art.figA2b.genTimePlot import Plot
from Parameters import *


if __name__ == '__main__':
    args = docopt(__doc__)

    if args['--fig'] == 'A2a':
        log = 'art/figA2a'
        mode = 'equation'
        model = 'models/Jet.json'
        init = [[0.8,1.0], [0.8,1,0]]
        timestamp = 2000
        my_sys = System(log, mode, model)
        my_sys.behaviour(init, timestamp)
    
    elif args['--fig'] == 'A2b':
        plot = Plot()
        plot.genPlot(True)

    elif args['--fig'] == 'A2c':
        log = 'art/figA2c'
        mode = 'equation'
        model = 'models/Jet.json'
        my_sys = System(log, mode, model)
        c = confidence(my_sys)
        c.varyC()

    elif args['--fig'] == 'A3a':
        log = 'art/figA3a/Jet.lg'
        mode = 'equation'
        model = 'models/Jet.json'
        my_sys = System(log, mode, model)
        my_sys.checkSafety()

    elif args['--fig'] == 'A3b':
        log = 'art/figA3b/Jet.lg'
        mode = 'equation'
        model = 'models/Jet.json'
        my_sys = System(log, mode, model)
        my_sys.checkSafety()

    elif args['--fig'] == 'A3c':
        log = 'art/figA3c/Jet.lg'
        mode = 'equation'
        model = 'models/Jet.json'
        my_sys = System(log, mode, model)
        my_sys.checkSafety()

    elif args['--fig'] == 'A3d':
        log = 'art/figA3d/Jet.lg'
        mode = 'equation'
        model = 'models/Jet.json'
        my_sys = System(log, mode, model)
        my_sys.checkSafety()

    elif args['--fig'] == 'A4a':
        log = 'art/figA4a/VDP.lg'
        mode = 'equation'
        model = 'models/VDP.json'
        my_sys = System(log, mode, model)
        my_sys.checkSafety()

    elif args['--fig'] == 'A4b':
        log = 'art/figA4b/VDP.lg'
        mode = 'equation'
        model = 'models/VDP.json'
        my_sys = System(log, mode, model)
        my_sys.checkSafety()

    elif args['--fig'] == 'A4c':
        log = 'art/figA4c/VDP.lg'
        mode = 'equation'
        model = 'models/VDP.json'
        my_sys = System(log, mode, model)
        my_sys.checkSafety()

    elif args['--fig'] == 'A4d':
        log = 'art/figA4d/VDP.lg'
        mode = 'equation'
        model = 'models/VDP.json'
        my_sys = System(log, mode, model)
        my_sys.checkSafety()
    
    elif args['--fig'] == 'B5':
        log = 'art/figB5/Jet.lg'
        mode = 'equation'
        model = 'models/Jet.json'
        init = [[0.8,1.0], [0.8,1,0]]
        timestamp = 2000
        prob = 5
        dtlog = 0.04
        my_sys = System(log, mode, model)
        my_sys.generateLog(init, timestamp, prob, dtlog = 0.04)

    else:
        warn("Invalid Command.")
        print(__doc__)
        sys.exit(1)
