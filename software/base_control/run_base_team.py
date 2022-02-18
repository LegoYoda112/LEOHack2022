import sys
import time

from numpy import absolute
from base_control import BaseControl, sat_msgs

import datetime

from math import sin, cos
import math

sys.path.append("./../sat_control/")
sys.path.append("./../../team/") 

import team_controller
sat_controller = team_controller.TeamController()

elapsed_time = 0.0

ctl = BaseControl("Test")

# ctl.connect_sat("localhost", 9000)
ctl.connect_sat("odo.local", 9000)

ctl.start_tracking()
ctl.start_heartbeat()

#team_ctl = TeamController()
#team_ctl.init()

input("Press enter to run team code")
ctl.update()
ctl.update()

control_message = sat_msgs.ControlMessage()
ctl.send_control(control_message)

while(1):
    ctl.update()
    
    print("running")

    # Update system state
    system_state = sat_msgs.SystemState()

    # Update current time
    current_time = datetime.datetime.now()
    system_state.absoluteTime.FromDatetime(self.current_time)

    # Update elapsed time
    elapsed_time = datetime.timedelta(seconds=self.dt)
    system_state.elapsedTime.FromTimedelta(self.elapsed_time)

    # Create control message
    control_message = sat_controller.run(ctl.sat_state, ctl.dead_sat_state, system_state)

    ctl.send_control(control_message)
    
    
    elapsed_time += 0.05
    time.sleep(0.05)

control_message = sat_msgs.ControlMessage()
ctl.send_control(control_message)