from sat_comms import SatComms

improt serial

# Start serial connection to rpi pico
self.ser = serial.Serial(serial_name, 115200, write_timeout = 0.001)
print(self.ser.name)

# Write twist message through serial
def writeTwist(x, y, theta):
    sendString = "%.2f %.2f %.2f\n" % (x, y, theta)

    # Flush input, output, then send string
    try:
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(bytes(sendString, "utf-8"))
    except Exception as e:
        print(e)

def drive(x, y, theta):
    self.writeTwist(x, y, theta)

def reset(self):
    self.writeTwist(0, 0, 0)

# Make new sat comms object
sat = SatComms("DAX")

# Register callbacks
sat.register_drive_callback(drive)
sat.register_reset_callback(reset)

# Start sat
sat.start()