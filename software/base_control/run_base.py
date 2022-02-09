import time
from base_control import BaseControl, sat_msgs

ctl = BaseControl("Test")

ctl.connect_sat("localhost", 9000)

ctl.start_heartbeat()

while(1):
    control_message = sat_msgs.ControlMessage()
    control_message.active = True

    ctl.send_control(control_message)

    time.sleep(1)