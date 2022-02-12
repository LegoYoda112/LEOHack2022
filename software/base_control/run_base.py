
import time
from base_control import BaseControl, sat_msgs

ctl = BaseControl("Test")

# ctl.connect_sat("localhost", 9000)
ctl.connect_sat("odo.local", 9000)

ctl.start_tracking()
ctl.start_heartbeat()

#team_ctl = TeamController()
#team_ctl.init()

input("Press enter to run team code")

# Wait for filter to converge
# for i in range (0, 40):
#     control_message = sat_msgs.ControlMessage()
#     ctl.send_control(control_message)
#     time.sleep(0.05)


while(1):
    ctl.update()

    control_message = sat_msgs.ControlMessage()
    control_message.active = True
    control_message.thrust.f_x =  -0.4 * (ctl.sat_state.pose.x - ctl.dead_sat_state.pose.x + 0.5) - 0.0 * (ctl.sat_state.twist.v_x)
    control_message.thrust.f_y = -0.4 * (ctl.sat_state.pose.y - ctl.dead_sat_state.pose.y + 0.0) - 0.0 * (ctl.sat_state.twist.v_y)
    control_message.thrust.tau =   - 0.3 * (ctl.sat_state.pose.theta - 3.1415/2) - 0.0 * (ctl.sat_state.twist.omega)
    # control_message.thrust.f_x = 0
    # control_message.thrust.f_y = 0
    control_message.time_step = 0.1

    # print(ctl.sat_state.pose.theta)

    # print((ctl.sat_state.pose.theta - 3.1415/2))

    # control_message = team_ctl.run(ctl.system_state, ctl.sat_state, ctl.dead_sat_state)


    print(ctl.dead_sat_state.pose)
    # print(control_message)

    ctl.send_control(control_message)

    time.sleep(0.1)