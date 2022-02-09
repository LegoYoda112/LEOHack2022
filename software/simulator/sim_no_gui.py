
import argparse, logging
from sim import Sim

import time

# ===================================== ARGS
# Create arg parser
parser = argparse.ArgumentParser()

# Verbase mode!
parser.add_argument(
    '-v', '--verbose',
    help="Verbose mode",
    action='store_const', dest='loglevel', const=logging.DEBUG,
    default = logging.INFO
)
# Parse args
args = parser.parse_args()

# Create simulator object
sim = Sim(args.loglevel, 3)
sim.start_meshcat()

input("Hit enter to continue running")

sim.start()

while(1):
    time.sleep(1)

sim.end()