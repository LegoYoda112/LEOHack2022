import sys
import os
sys.path.append("../sat_control/")

import argparse
import coloredlogs, logging

from sat_comms import SatComms

import numpy as np
import time

import meshcat
import meshcat.geometry as g
import meshcat.transformations as tf

import threading

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


# ===================================== LOGGING
# Make a new logger
logger = logging.getLogger('Sat sim')

# Install colored logs :)
coloredlogs.install(level=args.loglevel)

# Set the basic config up with correct log level
logging.basicConfig(level=args.loglevel)

# ===================================== MESH CAT
logger.info("Starting meshcat")
vis = meshcat.Visualizer()
vis.open()

# vis["robot"].set_object(g.Sphere(1), g.MeshLambertMaterial(color = 0xF33B12, reflectivity=0.9, opacity=1))
vis["robot2"].set_object(g.ObjMeshGeometry.from_file("3d_assets/Base.obj"), g.MeshPhongMaterial(color = 0xDD6442, transparent = False, opacity=1))
vis["robot"].set_object(g.ObjMeshGeometry.from_file("3d_assets/Base.obj"), g.MeshPhongMaterial(color = 0x73BE63, transparent = False, opacity=1))


sat_x = 0
sat_dx = 0
sat_y = 0
sat_dy = 0

# This is bad, do not do this, no one should ever do this
dt = 1.0 / 60.0

def sim_loop():
    global sat_x
    global sat_y
    global sat_dx
    global sat_dy

    while True:
        sat_x += sat_dx * dt
        sat_y += sat_dy * dt

        vis['robot'].set_transform(tf.translation_matrix([sat_x, sat_y, 0]))

        time.sleep(dt)

sim_thread = threading.Thread(target=sim_loop)
sim_thread.setDaemon(True)
sim_thread.start()

# ===================================== SAT COMMS
# Make new satalite
sat = SatComms("DAX_sim")

def drive(x, y, theta):
    global sat_dx
    global sat_dy

    logger.debug(f"{x}, {y}, {theta}")

    sat_dx = x / 30.0
    sat_dy = y / 30.0

sat.register_drive_callback(drive)

def reset():
    global sat_x
    global sat_y

    logger.debug("reset")

    sat_x = 0
    sat_y = 0

sat.register_reset_callback(reset)

logger.info("Starting sat comm thread")
sat.start()