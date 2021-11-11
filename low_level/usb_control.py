import serial
import time
ser = serial.Serial('COM3', 115200, write_timeout = 0.1)
print(ser.name)

# write a twist message to rp
def writeTwist(x, y, theta):
    print("send string")
    sendString = "%.2f %.2f %.2f\n" % (round(x, 2), round(y, 2), round(theta, 2))
    print(sendString)

    print("writing bytes")
    try:
        ser.write(bytes(sendString, "utf-8"))
    except WriteTimeoutError:
        print("write failed")

    print("written bytes")

import pygame

def deadzone(value, deadzone):
    if(abs(value) < deadzone):
        return 0
    return value

# try and except keyboard interrupt
try:
    writeTwist(0, 0, 0)

    pygame.init()
    pygame.joystick.init()

    print(pygame.joystick.get_count())
    joystick = pygame.joystick.Joystick(0)

    while True:
        #pygame.event.get()

        print("event pump")
        pygame.event.pump()

        print("get axis")
        axis0 = deadzone(joystick.get_axis(0), 0.1)
        axis1 = deadzone(joystick.get_axis(1), 0.1)
        axis2 = deadzone(joystick.get_axis(2), 0.1)
        axis3 = deadzone(joystick.get_axis(3), 0.1)
        
        print("write axis")
        writeTwist(-axis0 * 40.0, axis1 * 40.0, -axis3 / 5.0)

        print("sleep")
        time.sleep(0.05)
        

except KeyboardInterrupt:
    writeTwist(0, 0, 0)
    ser.close()
    print("\nSerial port closed")

ser.close()