
import time
from base_control import BaseControl, sat_msgs

from math import sin, cos
import math

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
ctl.send_control(control_message)
ctl.send_control(control_message)
ctl.send_control(control_message)

elapsed_time = 0.0

edge_offset = -0.5
dock_offset = -0.22
leave_offset = -1.0

time_to_edge = 2.0 # seconds

initial_pose = sat_msgs.Pose2D()
initial_pose.CopyFrom(ctl.sat_state.pose)

print("POSE")
print(ctl.sat_state.pose)

edge_pose = sat_msgs.Pose2D()
edge_pose.x = ctl.dead_sat_state.pose.x + edge_offset * cos(ctl.dead_sat_state.pose.theta - math.pi / 2)
edge_pose.y = ctl.dead_sat_state.pose.y + edge_offset * sin(ctl.dead_sat_state.pose.theta - math.pi / 2)
edge_pose.theta = ctl.dead_sat_state.pose.theta

time_to_dock = 4.0 # seconds

dock_pose = sat_msgs.Pose2D()
dock_pose.x = ctl.dead_sat_state.pose.x + dock_offset * cos(ctl.dead_sat_state.pose.theta - math.pi / 2)
dock_pose.y = ctl.dead_sat_state.pose.y + dock_offset * sin(ctl.dead_sat_state.pose.theta - math.pi / 2)
dock_pose.theta = ctl.dead_sat_state.pose.theta


time_to_pull = 5.0 # seconds

pull_pose = sat_msgs.Pose2D()
pull_pose.x = ctl.dead_sat_state.pose.x + leave_offset * cos(ctl.dead_sat_state.pose.theta - math.pi / 2)
pull_pose.y = ctl.dead_sat_state.pose.y + leave_offset * sin(ctl.dead_sat_state.pose.theta - math.pi / 2)
pull_pose.theta = ctl.dead_sat_state.pose.theta

def position_control(sat_pose, desired_pose):
    control_message = sat_msgs.ControlMessage()

    control_message.thrust.f_x =  0.3 * (sat_pose.x - desired_pose.x) - 0.0 * (ctl.sat_state.twist.v_x)
    control_message.thrust.f_y =  0.3 * (sat_pose.y - desired_pose.y + 0.0) - 0.0 * (ctl.sat_state.twist.v_y)
    control_message.thrust.tau =   - 0.4 * (sat_pose.theta - desired_pose.theta) - 0.0 * (ctl.sat_state.twist.omega)

    return control_message

def lerp_pose(pose0, pose1, f):
    ret_pose = sat_msgs.Pose2D()

    f = min(max(f, 0), 1)

    ret_pose.x = pose0.x * (1.0 - f) + pose1.x * f
    ret_pose.y = pose0.y * (1.0 - f) + pose1.y * f
    ret_pose.theta = pose0.theta * (1.0 - f) + pose1.theta * f

    return ret_pose

# def lerp_pose_over_time(pose0, pose1, move_time):
#     elapsed_time = 0.0

#     timestep = 0.05

#     for(t in np.arange(0, time, timestep)):
#         desired_pose = lerp_pose(pose0, pose1, (t) / move_time)



#         time.sleep(timestep)

servo_states = sat_msgs.ServoStates()

team_dock = {}
team_undock = {}

team_num = 10

team_dock[10] = [0.5, 0, 0]
team_undock[10] = [1, 0, 0]

team_undock[3] = [0.4, 0.6, 0]
team_dock[3] = [0.15, 0.15, 0]

servo_states.servo1 = team_undock[team_num][0]
servo_states.servo2 = team_undock[team_num][1]
servo_states.servo3 = team_undock[team_num][2]

while(1):
    ctl.update()

    # control_message = sat_msgs.ControlMessage()
    
    if(elapsed_time < time_to_edge):
        desired_pose = lerp_pose(initial_pose, edge_pose, elapsed_time / time_to_edge)

        # Team twist
        #servo_states.servo1 = 0.4

        # Team 3
        servo_states.servo1 = 0.3
        servo_states.servo2 = 0.5

        # Team 4
        # servo_states.servo1 = 0.3
        # servo_states.servo2 = 0.5
        # servo_states.servo3 = 0.3

        # servo_states.servo1 = 1
        # servo_states.servo2 = 1
        # servo_states.servo3 = 0.3

        servo_states.servo1 = team_undock[team_num][0]
        servo_states.servo2 = team_undock[team_num][1]
        servo_states.servo3 = team_undock[team_num][2]

        print("LERP FACTOR: ", elapsed_time / time_to_edge)

    elif(elapsed_time < time_to_edge + time_to_dock):
        desired_pose = lerp_pose(edge_pose, dock_pose, (elapsed_time - time_to_edge) / time_to_dock)

        # Team twist
        #servo_states.servo1 = 0.4

        # Team 3
        servo_states.servo1 = 0.3
        servo_states.servo2 = 0.5

        # Team 4
        # servo_states.servo1 = 0.3
        # servo_states.servo2 = 0.5
        # servo_states.servo3 = 0.3

        servo_states.servo1 = team_undock[team_num][0]
        servo_states.servo2 = team_undock[team_num][1]
        servo_states.servo3 = team_undock[team_num][2]

        print("LERP FACTOR: ", (elapsed_time - time_to_edge) / time_to_dock)


    elif(elapsed_time < time_to_edge + time_to_dock + time_to_pull):
        desired_pose = lerp_pose(dock_pose, pull_pose, (elapsed_time - time_to_edge - time_to_dock) / time_to_pull)
        #servo_states.servo1  = 1

        # Team 3
        servo_states.servo1 = 0.2
        servo_states.servo2 = 0.4

        # Team 4
        #servo_states.servo1 = 0.0
        #servo_states.servo2 = 0.0
        #servo_states.servo3 = 0.0

        servo_states.servo1 = team_dock[team_num][0]
        servo_states.servo2 = team_dock[team_num][1]
        servo_states.servo3 = team_dock[team_num][2]

    else:
        servo_states.servo1 = 0.4

        # Team 3
        servo_states.servo1 = 0.3
        servo_states.servo2 = 0.5

        # Team 4
        # servo_states.servo1 = 1
        # servo_states.servo2 = 1
        # servo_states.servo3 = 0.3

        servo_states.servo1 = team_undock[team_num][0]
        servo_states.servo2 = team_undock[team_num][1]
        servo_states.servo3 = team_undock[team_num][2]

    #desired_pose = edge_pose
    control_message = position_control(ctl.sat_state.pose, desired_pose)

    control_message.active = True
    control_message.servo_states.CopyFrom(servo_states)

    #print("==== pose ====")
    #print(ctl.sat_state.pose.x - dock_pose.x)
    #print(ctl.sat_state.pose.y - dock_pose.y)
    #print(ctl.sat_state.pose.theta - dock_pose.theta)

    
    
    #control_message.thrust.f_x =  -0.4 * (ctl.sat_state.pose.x - ctl.dead_sat_state.pose.x + 0.5) - 0.0 * (ctl.sat_state.twist.v_x)
    #control_message.thrust.f_y = -0.4 * (ctl.sat_state.pose.y - ctl.dead_sat_state.pose.y + 0.0) - 0.0 * (ctl.sat_state.twist.v_y)
    #control_message.thrust.tau =   - 0.3 * (ctl.sat_state.pose.theta - 3.1415/2) - 0.0 * (ctl.sat_state.twist.omega)
    # control_message.thrust.f_x = 0
    # control_message.thrust.f_y = 0
    control_message.time_step = 0.05

    # control_message.servo_states.servo1 = 0.7

    # print(ctl.sat_state.pose.theta)

    # print((ctl.sat_state.pose.theta - 3.1415/2))

    # control_message = team_ctl.run(ctl.system_state, ctl.sat_state, ctl.dead_sat_state)


    # print(ctl.dead_sat_state.pose)
    # print(control_message)
    # control_message = sat_msgs.ControlMessage()
    ctl.send_control(control_message)

    elapsed_time += 0.05
    time.sleep(0.05)

control_message = sat_msgs.ControlMessage()
ctl.send_control(control_message)