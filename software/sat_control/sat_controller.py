# Import abstract base class
from abc import ABC, abstractmethod


# Sat controller interface
import sys
sys.path.append("../msgs/")
sys.path.append("software/msgs/")

import sat_descrip_pb2 as sat_msgs

# The sat controller class contains all the required information
# to simulate and control a satalite

class SatControllerInterface(ABC):

    def __init__(self):
        
        # Make blank team info
        self.sat_description = sat_msgs.SatelliteDescription()

    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'run') and
                callable(subclass.run) and
                hasattr(subclass, 'init') and
                callable(subclass.init))

    def set_mass(self, mass):
        self.sat_description.mass = new_mass
    
    def set_inertia(self, inertia):
        self.sat_description.inertia = inertia

    @abstractmethod
    def run(self, system_state: sat_msgs.SystemState, satellite_state: sat_msgs.SataliteState) -> sat_msgs.ThrustCommand:
        raise NotImplementedError

    @abstractmethod
    def init(self) -> sat_msgs.TeamInfo:
        raise NotImplementedError
    
    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def abort(self) -> None:
        pass
    
    # Method to handle system state
    # Runs a basic state machine
    def handleState(self, system_state: sat_msgs.SystemState, satellite_state: sat_msgs.SataliteState):
        state = system_state.state
        
        # Basic state machine
        # Any state transition is allowed
        # =================== INIT STATE ===================
        if state == sat_msgs.SystemState.STATE_INIT:

            # Run team init and copy over team info
            team_info = self.init()
            self.description.team_info.CopyFrom(team_info)

            # Break
            break

        # =================== RUN STATE ===================
        elif state == sat_msgs.SystemState.STATE_RUN:

            # Run team controller and return resulting thrust command
            thrust_command = self.run(system_state, satellite_state)
            return thrust_command

            break

        # =================== ABORT STATE ===================
        elif state == sat_msgs.SystemState.STATE_ABORT:

            # Run team abort code
            self.abort()
            break

        # =================== RESET STATE ===================
        elif state == sat_msgs.SystemState.STATE_RESET:

            # Run team reset code
            self.reset()
            break
        
        return None