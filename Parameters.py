'''
Parameters required for the code
'''
import os,sys

'''
Please add the following line in ~/.bashrc
export MNTR_BB_ROOT_DIR = <YOUR PROJECT ROOT>
'''

PROJECT_ROOT = os.environ['MNTR_BB_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

LIB_PATH=PROJECT_ROOT+'/'+'lib/'
SRC_PATH=PROJECT_ROOT+'/'+'src/'
OUTPUT_PATH=PROJECT_ROOT+'/'+'output/'
PICKLE_PATH=PROJECT_ROOT+'/'+'pickles/'
DATA_PATH=PROJECT_ROOT+'/'+'data/'


PICKLE_FLAG=True
REFINE=True

B=100000
c=0.99

VIZ_PER_COVERAGE=20
VIZ = True

'''
PROBABILITY_LOG=11
DT=0.01
DELTA_STATE=0.004
DELTA_LOG=0.2
'''


'''
PROBABILITY_LOG=5
DT=0.01
DELTA_STATE=0.002
DELTA_LOG=0.02
'''


'''
Colors for terminal messages
'''
class msg:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def info(s):    print(f"{msg.OKCYAN}[INFO]{msg.ENDC} {s}")
def note(s):    print(f"{msg.OKBLUE}[INFO]{msg.ENDC} {s}")
def ok(s):      print(f"{msg.OKGREEN}[SUCCESS]{msg.ENDC} {s}")
def warn(s):    print(f"{msg.WARNING}[WARN]{msg.ENDC} {s}")
def die(s, hint=None, code=2):
    print(f"{msg.FAIL}[ERROR]{msg.ENDC} {s}")
    if hint:
        print(f"{msg.WARNING}[HINT]{msg.ENDC} {hint}")
    sys.exit(code)


