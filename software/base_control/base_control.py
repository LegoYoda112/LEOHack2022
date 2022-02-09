import time
import threading

import zmq

import sys
sys.path.append("../msgs/")
sys.path.append("software/msgs/")
import sat_descrip_pb2 as sat_msgs

class SatConnection:
    """ Stores sat connection information """
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port

class BaseControl:
    """ Class to run base control """
    def __init__(self, name):
        self.name = name

        self.sat = None

        self.heartbeat_thread = None

        self.context = zmq.Context()

        # Make a thread lock to prevent multiple threads from
        # accessing the socket at the same time
        self.comms_lock = threading.Lock()

    def connect_socket(self, ip, port):
        """ Connects to specified socket """
        self.send_socket = self.context.socket(zmq.REQ)
        self.send_socket.setsockopt(zmq.LINGER, 0)
        self.send_socket.connect("tcp://{}:{}".format(ip, port))

    def send_msg(self, msg, data):
        """ Sends a byte message to the sat, msg must be 3 characters long """
        print()

        if isinstance(data, bytes):
            print(data)
            self.send_socket.send(msg.encode("utf-8") + data)
        else:
            self.send_socket.send(msg.encode("utf-8") + data.encode("utf-8"))

    def connect_sat(self, ip, port, timeout = 1):
        """ Connects to specified sat """
        # Connect to socket and send hello message
        self.connect_socket(ip, port)
        self.send_msg("INI", "Greetings")

        # Start a poller to create a recv with a timeout
        poller = zmq.Poller()
        poller.register(self.send_socket, zmq.POLLIN)

        events = poller.poll(timeout * 1000)

        # DEBUG: print length of recived messages
        print(len(events))

        # If no messages are received, say something broke
        if(len(events) == 0):
            print("Connection Failed")
            self.send_socket.close()

            raise Exception("No satalite at ip")

            return (False, "")

        else:
            print("Sucsessful connection")

            recv_string = events[0][0].recv().decode("utf-8")
            sat_name = recv_string.split(" ")[1]

            self.sat = SatConnection(sat_name, ip, port)
            print(self.sat)

            return (True, sat_name)

    def ping(self, timeout):
        """Pings the sat""" 
        self.comms_lock.acquire()
        # print(" ==== Ping lock")

        # Send message
        self.send_msg("HBB", "ping")

        # Register a poller to send with a timeout
        poller = zmq.Poller()
        poller.register(self.send_socket, zmq.POLLIN)

        events = poller.poll(timeout * 1000)

        # print(" ==== Ping unlock")
        self.comms_lock.release()

        # Debug, 
        print(len(events))

        if(len(events) == 0):
            print("Connection Failed")
            return False
        else:
            reply = events[0][0].recv().decode("utf-8")
            print(reply)
            return True

    # Heartbeat to check if 
    def heartbeat(self):
        """Heartbeat thread that pings the satalite every second"""
        # Loop that pings the sat every second
        while(True):
            print("ping!")
            status = self.ping(5) # ping with timeout of 5 seconds

            time.sleep(1) # wait one second

    def start_heartbeat(self):
        """Starts the heartbeat thread"""
        # Create the heartbeat threat and start it
        self.heartbeat_thread = threading.Thread(target = self.heartbeat, args=(), daemon = True)
        self.heartbeat_thread.start()

    def send_control(self, control_message):
        """ Sends control message """
        self.comms_lock.acquire()
        # print(" ==== Control lock")

        t0 = time.time()


        self.send_msg("CTL", control_message.SerializeToString())

        state_msg = sat_msgs.SataliteState()
        rcv_msg = self.send_socket.recv()
        state_msg.ParseFromString(rcv_msg)

        print(state_msg)

        t1 = time.time()

        print("Round trip time", round((t1 - t0) * 1000), "ms")

        # print(" ==== Control unlock")
        self.comms_lock.release()