# LEOHack 2021


## Handshake process
When a team first connects into the satellite "network", a handshake process is performed to ensure a proper connection has been established as well as to update the team control, base station control and the satellite control. Generally teams will not have to worry about the specifics of this process, but here is the outline:
- Team control requests an update from base control.
- Base control replies with a mostly populated SataliteDescription, giving the team the mass, inertia, ip etc.
- The team code fills out their name and id, and sends it back to the base control.
- The base control updates itself and sends the description to the satellite
- The satellite responds to the base station and team laptop with a success message, informing both that the link has been set up.

pip install zmq
pip install protobuf
pip install colored logs
pip install numpy
pip install meshcat
pip install argparse