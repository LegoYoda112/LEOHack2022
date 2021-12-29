import sys
import os

print(os.getcwd())

sys.path.append("../sat_control/")
import team_controller
from sat_controller import sat_msgs

import importlib

import coloredlogs, logging

import numpy as np
import time

import meshcat
import meshcat.geometry as g
import meshcat.transformations as tf

import threading

class Sim():
    
    def __init__(self, logging_level):

        # Install colored logs :)
        coloredlogs.install(level=logging_level)

        # Set the basic config up with correct log level
        logging.basicConfig(level=logging_level)

        # Make a new logger
        self.logger = logging.getLogger('Sat sim')

        # Sat controller
        self.sat_controller = None
        self.loadTeamController()


    def start_meshcat(self):
        # Open meshcat window
        self.vis = meshcat.Visualizer()
        self.vis.open()

        # Add satellites
        self.vis["dead_sat"].set_object(g.ObjMeshGeometry.from_file("3d_assets/Base.obj"), g.MeshPhongMaterial(color = 0xDD6442, transparent = False, opacity=1))
        self.vis["team_sat"].set_object(g.ObjMeshGeometry.from_file("3d_assets/Base.obj"), g.MeshPhongMaterial(color = 0x73BE63, transparent = False, opacity=1))

        self.logger.debug("Meshcat started")

    def loadTeamController(self):
        # Reload team controller module
        importlib.reload(team_controller)
        self.sat_controller = team_controller.TeamController()

        self.logger.debug("Reloaded team controller")

    def start(self):
        self.logger.info("Starting simulation")

    def end(self):
        self.logger.info("Ending simulation")