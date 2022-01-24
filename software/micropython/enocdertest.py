from motors import Motors
m = Motors()

import time
from math import sin, cos

ticks_prev = time.ticks_us()
ticks_diff = 0
time_taken = 0

loop_hz = 20
period_s = (1.0 / loop_hz)
period_ms = int(period_s * 1000)

perf_checker = True

robot_radius = 67.4 / 100.0 # m
wheel_dia = 80.0 / 1000.0 # m

J3 = wheel_dia / robot_radius 

J = [[-0.03, 0.015, 0.015],
     [0.0, -0.0259808, 0.0259808],
     [J3, J3, J3]]

x = 0.0
y = 0.0
theta = 0.0

while(1):
    if perf_checker:
        ticks_now = time.ticks_ms()
        ticks_diff = time.ticks_diff(ticks_now, ticks_prev)
        ticks_prev = time.ticks_ms()
        
        print("Loop time: ", ticks_diff)
        print("Code time: ", time_taken)
    
    start_ticks = time.ticks_ms()
    
    q_1 = m.motor1.encoder.getVelRot(period_s)
    q_2 = m.motor2.encoder.getVelRot(period_s)
    q_3 = m.motor3.encoder.getVelRot(period_s)
    
    vel_x = q_1 * J[0][0] + q_2 * J[0][1] + q_3 * J[0][2]
    vel_y = q_1 * J[1][0] + q_2 * J[1][1] + q_3 * J[1][2]
    omega = q_1 * J[2][0] + q_2 * J[2][1] + q_3 * J[2][2]
    
    dx = vel_x * period_s
    dy = vel_y * period_s
    
    x += dx * cos(theta) + dy * sin(theta) 
    y += dx * sin(theta) - dy * cos(theta)
    theta += omega * period_s
    
    print("X", x)
    print("Y", y)
    print("Theta", theta)
    
    end_ticks = time.ticks_ms()
    time_taken = time.ticks_diff(end_ticks, start_ticks)
    
    time.sleep(period_s - time_taken / 1000.0)
    
    
