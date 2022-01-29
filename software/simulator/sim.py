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
import time

from enum import Enum

class SimState(Enum):
    STOPPED = 0
    RUNNING = 1
    PAUSED = 2

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
        self.load_team_controller()

        # Sim thread
        # TODO: Make not a daemon thread?
        self.sim_thread = None
        self.sim_thread_lock = threading.Lock()

        # Sim state enum
        self.sim_state = SimState.STOPPED

        # Boolean to break thread if stop is called
        self.kill_thread = False

        # Sim dt (seconds)
        self.dt = 0.01
        self.sat_state = sat_msgs.SataliteState()
        self.dead_sat_state = sat_msgs.SataliteState()
        self.system_state = sat_msgs.SystemState()

        # Zero out all states
        self.reset()

    def start_meshcat(self):
        # Open meshcat window
        self.vis = meshcat.Visualizer()
        self.vis.open()

        # Add satellites
        self.vis["dead_sat"].set_object(g.ObjMeshGeometry.from_file("3d_assets/Base.obj"), g.MeshPhongMaterial(color = 0xDD6442, transparent = False, opacity=1))
        self.logger.debug("Added dead sat")
        self.vis["team_sat"].set_object(g.ObjMeshGeometry.from_file("3d_assets/Base.obj"), g.MeshPhongMaterial(color = 0x73BE63, transparent = False, opacity=1))
        self.logger.debug("Added team sat")

        self.logger.info("Meshcat started")

    def load_team_controller(self):
        # Reload team controller module
        importlib.reload(team_controller)
        self.sat_controller = team_controller.TeamController()

        self.logger.debug("Reloaded team controller")

    def sim_thread_function(self):
        self.logger.info("Starting sim thread")

        while True:
            # Acquire thread lock
            self.sim_thread_lock.acquire()

            if self.kill_thread:
                self.logger.debug("Sim thread killed")
                break

            # SIM MATH

            # Integrate
            self.sat_state.pose.x += self.sat_state.twist.v_x * self.dt
            self.sat_state.pose.y += self.sat_state.twist.v_y * self.dt
            self.sat_state.pose.theta += self.sat_state.twist.omega * self.dt

            # Run team controller
            thrust_command = self.sat_controller.run(self.system_state, self.sat_state)

            if(thrust_command == None):
                self.logger.error("Error encountered in team controller")
            else:
                # Integrate
                self.sat_state.twist.v_x += thrust_command.thrust.f_x * self.dt
                self.sat_state.twist.v_y += thrust_command.thrust.f_y * self.dt
                self.sat_state.twist.omega += thrust_command.thrust.tau * self.dt

            # Update visualizer
            self.vis["team_sat"].set_transform(
                tf.translation_matrix([
                    self.sat_state.pose.x, 
                    self.sat_state.pose.y, 
                    0]).dot(tf.rotation_matrix(self.sat_state.pose.theta, 
                [0, 0, 1])))

                # Update visualizer
            self.vis["dead_sat"].set_transform(
                tf.translation_matrix([
                    self.dead_sat_state.pose.x, 
                    self.dead_sat_state.pose.y, 
                    0]).dot(tf.rotation_matrix(self.dead_sat_state.pose.theta, 
                [0, 0, 1])))

            self.logger.debug("Running thread")
            
            # Release thread lock
            self.sim_thread_lock.release()

            # Wait amount of time
            time.sleep(self.dt)

        self.logger.info("Simulation ended")

    def start(self):
        self.logger.info("Starting simulation")

        # Reset all simulation constants
        self.reset()

        # Create and start a new sim thread
        self.sim_thread = threading.Thread(target=self.sim_thread_function, daemon=True)
        self.sim_thread.start()

        # Set state to running
        self.sim_state = SimState.RUNNING

    def pause(self):
        self.logger.info("Pausing simulation")

        # If sim is running, pause it
        if self.sim_state == SimState.RUNNING:
            # Acquire thread lock
            self.sim_thread_lock.acquire()

            # Set state to paused
            self.sim_state = SimState.PAUSED

        # Warn if thread is already paused
        elif self.sim_state == SimState.PAUSED:
            self.logger.warn("Simulation already paused")

        # Warn if thread is not running
        elif self.sim_state == SimState.STOPPED:
            self.logger.warn("Simulation is not running")

    def play(self):
        self.logger.info("Playing simulation")

        # If sim is paused, play it
        if self.sim_state == SimState.PAUSED:

            # Release thread lock
            self.sim_thread_lock.release()

            # Set state to paused
            self.sim_state = SimState.RUNNING
        
        # Warn if thread is not paused
        elif self.sim_state == SimState.RUNNING:
            self.logger.warn("Simulation is already playing")
        
        # Warn if thread is not running
        elif self.sim_state == SimState.STOPPED:
            self.logger.warn("Simulation is has been stopped")

    def reset(self):
        self.pause()
        self.logger.info("Resetting simulation")

        # Reset simulation

        # Zero out the sat state
        self.sat_state.pose.x = 0.0
        self.sat_state.pose.y = 0.0
        self.sat_state.pose.theta = 0.0

        self.sat_state.twist.v_x = 0.0
        self.sat_state.twist.v_y = 0.0
        self.sat_state.twist.omega = 0.0

        # Init the dead sat state
        self.dead_sat_state.pose.x = 2.0
        self.dead_sat_state.pose.y = 4.0
        self.dead_sat_state.pose.theta = -2.0

        self.dead_sat_state.twist.v_x = 0.0
        self.dead_sat_state.twist.v_y = 0.0
        self.dead_sat_state.twist.omega = 0.0

        # Run team init code
        self.sat_controller.team_init()

    def reload(self):
        self.logger.info("Reloading controller")

        # Reload team controller
        self.load_team_controller()
        self.reset()

    def end(self):
        self.logger.info("Ending simulation")

        if self.sim_state == SimState.STOPPED:
            self.logger.warn("Simulation is not running")
            return

        # If sim is running, acquire thread lock
        if self.sim_state == SimState.RUNNING:
            # Acquire thread lock
            self.sim_thread_lock.acquire()

        self.kill_thread = True
        
        # Release thread lock and let thread end itself
        self.sim_thread_lock.release()

        self.sim_thread.join()

        # Set state to stopped
        self.sim_state = SimState.STOPPED