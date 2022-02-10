import socket
from sat_comms import SatComms

hostname = socket.gethostname()

print(f"Sat control started on {hostname}.local")
print(socket.gethostbyname(hostname))

comms = SatComms(hostname)
comms.start("COM2")