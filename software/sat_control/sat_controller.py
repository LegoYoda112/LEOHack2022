# Import abstract base class
from abc import ABC, abstractmethod

# Sat controller interface
import sys
sys.path.append("../msgs/")
sys.path.append("software/msgs/")

import sat_descrip_pb2 as sat_msgs

class SatController(ABC):
    @abstractmethod
    def run(self, system_state: sat_msgs.SystemState, satellite_state: sat_msgs.SataliteState) -> sat_msgs.ThrustCommand:
        pass

    @abstractmethod
    def init(self) -> sat_msgs.TeamInfo:
        pass
    
    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def abort(self) -> None:
        pass