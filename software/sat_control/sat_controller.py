# Import abstract base class
from abc import ABC, abstractmethod

# Import sat messages protobuf
import sys
sys.path.append("../msgs/")
sys.path.append("software/msgs/")
import sat_descrip_pb2 as sat_msgs

# Import logging and traceback library
import logging
import traceback

# The sat controller class contains all the required information
# to control and simulate a "Satellite"

# Teams will implement various functions of this class
# to provide the control necessary to run the Satellite

class SatControllerInterface(ABC):
    """ Interface to build sat controllers on """

    def __init__(self):
        
        # Make a blank sat_description
        self.sat_description = sat_msgs.SatelliteDescription()

        # Make logger
        self.logger = logging.getLogger(__name__)

    # Check if abstract methods have been implemented
    def __subclasshook__(self, subclass):
        return (hasattr(subclass, 'run') and
                callable(subclass.run) and
                hasattr(subclass, 'init') and
                callable(subclass.init))

    # ====================== ABSTRACT TEAM FUNCTIONS
    # Abstract run method, the team will implement this
    @abstractmethod
    def team_run(self, system_state: sat_msgs.SystemState, satellite_state: sat_msgs.SatelliteState) -> sat_msgs.ControlMessage:
        raise NotImplementedError

    # Abstract init method, the team will implement this
    @abstractmethod
    def team_init(self) -> sat_msgs.TeamInfo:
        raise NotImplementedError
    
    # Abstract reset method, the team will implement this
    @abstractmethod
    def team_reset(self) -> None:
        pass

    # ====================== CONTROLLER FUNCTIONS
    def init(self) -> sat_msgs.TeamInfo:

        team_info = self.team_init()
        
        self.sat_description.teamInfo.CopyFrom(team_info)

        self.logger.info(f'Sat controller initialized ' +
                        f'for team {team_info.teamName} ' +
                        f'with team ID {team_info.teamID} ')

        return team_info

    def run(self, system_state: sat_msgs.SystemState, satellite_state: sat_msgs.SatelliteState, dead_sat_state: sat_msgs.SatelliteState) -> sat_msgs.ControlMessage:
        try:
            thrust_cmd = self.team_run(system_state, satellite_state, dead_sat_state)
        except Exception as e:
            self.logger.error(f'Exception in run function.')
            self.logger.error(traceback.format_exc())
            thrust_cmd = None
        return thrust_cmd

    def reset(self):
        self.team_reset()

    # ====================== GETTERS AND SETTERS
    def set_mass(self, mass):
        self.sat_description.mass = mass
    
    def set_inertia(self, inertia):
        self.sat_description.inertia = inertia