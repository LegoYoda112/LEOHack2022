import time
from base_control import BaseControl, sat_msgs

ctl = BaseControl("Test")

ctl.connect_sat("localhost", 9000)

ctl.start_heartbeat()

while(1):
    control_message = sat_msgs.ControlMessage()
    control_message.active = True
    control_message.thrust.f_x = 0.5
    control_message.time_step = 0.1

    ctl.send_control(control_message)

    time.sleep(0.1)