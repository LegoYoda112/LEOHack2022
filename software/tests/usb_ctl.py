import serial
import time

ser = serial.Serial('/dev/ttyACM0', write_timeout=0.1)
print("connected: ", ser.name)

ser.write(bytes("0.0 0.0 0.0\n", "utf-8"))
print(ser.readline())

ser.close()
