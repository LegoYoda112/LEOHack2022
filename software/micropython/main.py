import machine
import time

led0 = machine.Pin(25, machine.Pin.OUT)
led1 = machine.Pin(2, machine.Pin.OUT)
led2 = machine.Pin(1, machine.Pin.OUT)
led3 = machine.Pin(0, machine.Pin.OUT)

import micropython
import select
import sys

from kinematics import Kinematics

# micropython.kbd_intr(-1)

led0.off()
led1.off()
led2.off()
led3.off()

# Loop constants
loop_hz = 20
period_s = (1.0 / loop_hz)
period_ms = int(period_s * 1000)

k = Kinematics()

x_vel = 0
y_vel = 0
omega = 0

while True:
    
    # For loop timing
    start_ticks = time.ticks_ms()
    
    try:
        while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline()
            if(line == '\n'):
                break
            
            values = line.split()
        
            
            led1.on()
            
            cmd = values[0]
            if(cmd == "odom"):
                print("%0.3f %0.3f %0.3f %0.3f %0.3f %0.3f\n" % (k.x, k.y, k.theta, k.vel_x, k.vel_y, k.omega))
                
            elif(cmd == "theta"):
                k.theta = float(values[1])
                
            elif(cmd == "ctl"):
                x = float(values[1])
                y = float(values[2])
                theta = -float(values[3])
                
                # print("%0.3f %0.3f %0.3f" % (x, y, theta))
                
                x_vel = x
                y_vel = y
                omega = theta
            else:
                led2.on()
        
        # Turn status leds off
        led1.off()
        led2.off()
    except ValueError:
        # Error!
        led3.on()
    
    k.twistVelAbsolute(x_vel, y_vel, omega)
    k.updateOdom(period_s)
    
    # print(k.x)
    # print(k.vel_x)
    # print(k.y)
    # print(k.theta)
    # print()
        
    # Calculate how long code took to run and sleep remaining time
    end_ticks = time.ticks_ms()
    time_taken = time.ticks_diff(end_ticks, start_ticks)
    
    time.sleep(period_s - time_taken / 1000.0)


