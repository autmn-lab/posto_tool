#!/usr/bin/env python3
"""
Usage:
    artEvalNN.py --fig=<figno>

"""

from docopt import docopt
import ast
import os
import re
import sys

from System import System
from dev.ModelANN import sys_obj
from Parameters import *


if __name__ == '__main__':
    args = docopt(__doc__)

    if args['--fig'] == 'B6a':
        sys_obj.log_path = 'art/figB6a/MCcontroller.lg'
    
    elif args['--fig'] == 'B6b':
        sys_obj.log_path = 'art/figB6b/MCcontroller.lg'

    elif args['--fig'] == 'B6c':
        sys_obj.log_path = 'art/figB6c/MCcontroller.lg'

    elif args['--fig'] == 'B6d':
        sys_obj.log_path = 'art/figB6d/MCcontroller.lg'

    else:
        warn("Invalid Command.")
        print(__doc__)
        sys.exit(1)

    sys_obj.checkSafety()