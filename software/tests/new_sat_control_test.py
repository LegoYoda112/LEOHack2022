import sys
sys.path.append("../sat_control/")

from sat_comms import SatComms

sat = SatComms("DAX")

def drive(x, y, theta):
    print(x, y, theta)

sat.register_drive_callback(drive)

def reset():
    print("reset")

sat.register_reset_callback(reset)


sat.start()