import time
from base_control import BaseControl, sat_msgs

ctl = BaseControl("Test")

# ctl.connect_sat("localhost", 9000)
ctl.connect_sat("192.168.17.13", 9000)

ctl.start_tracking()
ctl.start_heartbeat()

while(1):
    control_message = sat_msgs.ControlMessage()
    control_message.active = True
    #control_message.thrust.f_x = - 2.0 * (ctl.sat_state.pose.x + 0.0) - 8.0 * (ctl.sat_state.twist.v_x)
    #control_message.thrust.f_y = + 2.0 * (ctl.sat_state.pose.y + 0.0) - 8.0 * (ctl.sat_state.twist.v_y)
    control_message.thrust.f_x = 0
    control_message.thrust.f_y = 0
    control_message.time_step = 0.1

    print(ctl.sat_state.pose)

    ctl.send_control(control_message)

    time.sleep(0.1)