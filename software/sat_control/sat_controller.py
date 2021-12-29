# Import abstract base class
from abc import ABC, abstractmethod

# Import sat messages protobuf
import sys
sys.path.append("../msgs/")
sys.path.append("software/msgs/")
import sat_descrip_pb2 as sat_msgs

# Import logging library
import logging

# The sat controller class contains all the required information
# to control and simulate a "satalite"

# Teams will implement various functions of this class
# to provide the control necessary to run the satalite

class SatControllerInterface(ABC):

    def __init__(self):
        
        # Make a blank sat_description
        self.sat_description = sat_msgs.SatelliteDescription()

        # Make logger
        self.logger = logging.getLogger(__name__)

    # Check if abstract methods have been implemented
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'run') and
                callable(subclass.run) and
                hasattr(subclass, 'init') and
                callable(subclass.init))

    # Abstract run method, the team will implement this
    @abstractmethod
    def team_run(self, system_state: sat_msgs.SystemState, satellite_state: sat_msgs.SataliteState) -> sat_msgs.ThrustCommand:
        raise NotImplementedError

    # Abstract init method, the team will implement this
    @abstractmethod
    def team_init(self) -> sat_msgs.TeamInfo:
        raise NotImplementedError
    
    # Abstract reset method, the team will implement this
    @abstractmethod
    def team_reset(self) -> None:
        pass
    
    # Method to handle system state
    # Runs a basic state machine
    def handleState(self, system_state: sat_msgs.SystemState, satellite_state: sat_msgs.SataliteState):
        state = system_state.state
        
        # Basic state machine
        # Any state transition is allowed
        # =================== INIT STATE ===================
        if state == sat_msgs.SystemState.INIT:

            # Run team init and copy over team info
            team_info = self.init()
            self.sat_description.teamInfo.CopyFrom(team_info)

            self.logger.info(f'Sat controller initialized ' +
                            f'for team {team_info.teamName} ' +
                            f'with team ID {team_info.teamID} ')

            return

        # =================== RUN STATE ===================
        elif state == sat_msgs.SystemState.RUN:

            # Run team controller and return resulting thrust command
            thrust_command = self.run(system_state, satellite_state)
            return thrust_command

        # =================== ABORT STATE ===================
        elif state == sat_msgs.SystemState.ABORT:

            # Run team abort code
            self.abort()
            return

        # =================== RESET STATE ===================
        elif state == sat_msgs.SystemState.RESET:

            # Run team reset code
            self.reset()
            return
        
        return None

    # Getters and setters
    def set_mass(self, mass):
        self.sat_description.mass = mass
    
    def set_inertia(self, inertia):
        self.sat_description.inertia = inertia