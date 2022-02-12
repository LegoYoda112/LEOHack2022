from re import T
import sys
import os

print(os.getcwd())

sys.path.append("../../team/")
sys.path.append("./team")
sys.path.append("./software/sat_control")
sys.path.append("../sat_control")
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
import datetime
from google.protobuf.timestamp_pb2 import Timestamp

from enum import Enum

from math import sin, cos
import math

class SimState(Enum):
    """ Simulator state enum """
    STOPPED = 0
    RUNNING = 1
    PAUSED = 2

class Sim():
    """Sat simulator"""
    
    def __init__(self, logging_level, challenge_level = 1, timestep = 0.05):
        """Takes in logging level and constructs a sim object"""

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
        self.dt = timestep
        self.sat_state = sat_msgs.SatelliteState()
        self.dead_sat_state = sat_msgs.SatelliteState()
        self.system_state = sat_msgs.SystemState()

        # The start time of each sim run to calculate elapsed time
        self.start_time = None

        # Sets challange level (adjusts how dead sat operates)
        self.challenge_level = challenge_level

        self.draw_targets = True

        # Zero out all states
        self.reset()

    def start_meshcat(self):
        """ Starts meshcat and loads in sats """
        # Open meshcat window
        self.vis = meshcat.Visualizer()
        self.vis.open()

        self.vis["/Background"].set_property("top_color", [0, 0, 0])

        # Add satellites
        self.vis["dead_sat"].set_object(g.ObjMeshGeometry.from_file("software/simulator/3d_assets/Base.obj"), g.MeshPhongMaterial(color = 0xDD6442, transparent = False, opacity=1))
        self.logger.debug("Added dead sat")
        self.vis["team_sat"].set_object(g.ObjMeshGeometry.from_file("software/simulator/3d_assets/Base.obj"), g.MeshPhongMaterial(color = 0x73BE63, transparent = False, opacity=1))
        self.logger.debug("Added team sat")

        if(self.draw_targets):
            self.vis['target'].set_object(g.Sphere(0.05), g.MeshPhongMaterial(color = 0x73BE63, transparent = True, opacity=0.2))

        self.logger.info("Meshcat started")

    def load_team_controller(self):
        """ Loads the teamcontroller """
        # Reload team controller module
        importlib.reload(team_controller)
        self.sat_controller = team_controller.TeamController()

        self.logger.debug("Reloaded team controller")

    def sim_thread_function(self):
        """ Sim loop thread """
        self.logger.info("Starting sim thread")

        while True:
            # Acquire thread lock
            self.sim_thread_lock.acquire()

            if self.kill_thread:
                self.logger.debug("Sim thread killed")
                break
            
            # Update system state

            # Update current time
            # from: https://stackoverflow.com/questions/49161633/how-do-i-create-a-protobuf3-timestamp-in-python
            self.current_time = datetime.datetime.now()
            self.system_state.absoluteTime.FromDatetime(self.current_time)

            # Update elapsed time
            self.elapsed_time += datetime.timedelta(seconds=self.dt)
            self.system_state.elapsedTime.FromTimedelta(self.elapsed_time)

            # SIM MATH

            # Update dead sat pose
            self.update_dead_sat_pose()

            # Integrate
            self.sat_state.pose.x += self.sat_state.twist.v_x * self.dt
            self.sat_state.pose.y += self.sat_state.twist.v_y * self.dt
            self.sat_state.pose.theta += self.sat_state.twist.omega * self.dt

            # Run team controller
            thrust_command = self.sat_controller.run(self.system_state, self.sat_state, self.dead_sat_state)

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
                    0]).dot(tf.rotation_matrix(self.sat_state.pose.theta + math.pi / 2, 
                [0, 0, 1])))

                # Update visualizer
            self.vis["dead_sat"].set_transform(
                tf.translation_matrix([
                    self.dead_sat_state.pose.x, 
                    self.dead_sat_state.pose.y, 
                    0]).dot(tf.rotation_matrix(self.dead_sat_state.pose.theta + math.pi / 2, 
                [0, 0, 1])))

            self.logger.debug("Running thread")

            # Check for docking
            docked = self.check_for_docking()
            if(docked):
                self.logger.info("Congrats! You have docked.")
            
            # Release thread lock
            self.sim_thread_lock.release()

            # Wait amount of time
            time.sleep(self.dt)

        self.logger.info("Simulation ended")

    def check_for_docking(self):
        """ Checks docking requirements """
        docked = True

        dead_x = self.dead_sat_state.pose.x
        dead_y = self.dead_sat_state.pose.y
        dead_theta = self.dead_sat_state.pose.theta

        # Local offsets and tolerances
        x_tolerance = 0.05

        y_offset = 0.25
        y_tolerance = 0.05

        theta_tolerance = 0.1

        # Global offsets
        x_target = dead_x + y_offset * cos(dead_theta - math.pi / 2)
        y_target = dead_y + y_offset * sin(dead_theta - math.pi / 2)

        x_error = abs(self.sat_state.pose.x - x_target)
        y_error = abs(self.sat_state.pose.y - y_target)
        theta_error = abs(self.sat_state.pose.theta % math.pi - dead_theta % math.pi)

        # Check position tolerance
        if(x_error < x_tolerance and y_error < y_tolerance):
            self.logger.info("Passing position tolerance!")
        else:
            docked = False

        # Check angular tolerance
        
        

        # Draw target
        if(self.draw_targets):
            # Update visualizer
            self.vis["target"].set_transform(
                tf.translation_matrix([
                    x_target, 
                    y_target, 
                    0]).dot(tf.rotation_matrix(0, 
                [0, 0, 1])))

        return docked

    def update_dead_sat_pose(self):
        """ Updates the dead sat pose based on challenge level """

        t = self.elapsed_time.total_seconds()
        
        if(self.challenge_level == 0):
            # LEVEL 0 = Stationary sat, no rotation
            self.dead_sat_state.pose.x = 1
            self.dead_sat_state.pose.y = -1
            self.dead_sat_state.pose.theta = - math.pi / 2
        elif(self.challenge_level == 1):
            # LEVEL 1 = Stationary sat
            self.dead_sat_state.pose.x = 1.5
            self.dead_sat_state.pose.y = -2.0 
            self.dead_sat_state.pose.theta = -1.8
        elif(self.challenge_level == 2):
            # LEVEL 2 = Translating sat
            self.dead_sat_state.twist.v_x = 0.04
            self.dead_sat_state.twist.v_y = -0.03
            self.dead_sat_state.twist.omega = 0.0

            self.dead_sat_state.pose.x = 0.5 + t * self.dead_sat_state.twist.v_x
            self.dead_sat_state.pose.y = -1.2 + t * self.dead_sat_state.twist.v_y 
            self.dead_sat_state.pose.theta = -0.3
        elif(self.challenge_level == 3):
            # LEVEL 2 = Translating sat
            self.dead_sat_state.twist.omega = 0.2

            self.dead_sat_state.pose.x = 0.2
            self.dead_sat_state.pose.y = -2.0
            self.dead_sat_state.pose.theta = -0.3 + t * self.dead_sat_state.twist.omega
        elif(self.challenge_level == 4):
            # LEVEL 3 Translating and rotating sat
            self.dead_sat_state.twist.v_x = 0.02
            self.dead_sat_state.twist.v_y = -0.01
            self.dead_sat_state.twist.omega = 0.05

            self.dead_sat_state.pose.x = 0.5 + t * self.dead_sat_state.twist.v_x
            self.dead_sat_state.pose.y = -0.2 + t * self.dead_sat_state.twist.v_y
            self.dead_sat_state.pose.theta = -0.4 + t * self.dead_sat_state.twist.omega

    def start(self):
        """ Starts the simulation """
        self.logger.info("Starting simulation")

        # Reset all simulation constants
        self.reset()

        # Create and start a new sim thread
        self.sim_thread = threading.Thread(target=self.sim_thread_function, daemon=True)
        self.sim_thread.start()

        # Set state to running
        self.sim_state = SimState.RUNNING

    def pause(self):
        """ Pauses the simulation """
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
        """ Plays the simulation """
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
        """ Resets the simulation """
        self.pause()
        self.logger.info("Resetting simulation")

        # Reset simulation

        # Zero elapsed time
        self.elapsed_time = datetime.timedelta(seconds=0)

        # Zero out the sat state
        self.sat_state.pose.x = -1.0
        self.sat_state.pose.y = -1.0
        self.sat_state.pose.theta = math.pi / 2

        self.sat_state.twist.v_x = 0.0
        self.sat_state.twist.v_y = 0.0
        self.sat_state.twist.omega = 0.0

        # Init the dead sat state
        self.update_dead_sat_pose()

        # Run team init code
        self.sat_controller.team_init()

    def reload(self):
        """ Reloads the team controller and resets"""
        self.logger.info("Reloading controller")

        # Reload team controller
        self.load_team_controller()
        self.reset()

    def end(self):
        """ Stops the simulation """
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