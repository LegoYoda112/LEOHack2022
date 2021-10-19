import zmq
import threading
import time

class SatConnection:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port

class BaseControl:
    def __init__(self, name):
        self.name = name

        self.sat = None

        self.heartbeat_thread = None

        self.context = zmq.Context()

    def connect_socket(self, ip, port):
        self.send_socket = self.context.socket(zmq.REQ)
        self.send_socket.setsockopt(zmq.LINGER, 0)
        self.send_socket.connect("tcp://{}:{}".format(ip, port))
    
    def send_msg(self, msg_data):
        self.send_socket.send_string(msg_data)
    
    def connect_sat(self, ip, port, timeout = 1):
        # Connect to socket and send hello message
        self.connect_socket(ip, port)
        self.send_msg("hello!")

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

            return (False, "")

        else:
            print("Sucsessful connection")

            sat_name = events[0][0].recv().decode("utf-8")

            self.sat = SatConnection(sat_name, ip, port)
            print(self.sat)

            return (True, sat_name)

    def ping(self, timeout):
        # Send message
        self.send_msg("ping")

        # Register a poller to send with a timeout
        poller = zmq.Poller()
        poller.register(self.send_socket, zmq.POLLIN)

        events = poller.poll(timeout * 1000)

        # Debug, 
        print(len(events))

        if(len(events) == 0):
            print("Connection Failed")
            return False
        else:
            reply = events[0][0].recv().decode("utf-8")
            print(reply)
            return True

    def heartbeat(self, callback):
        # Loop that pings the sat every second
        while(True):
            print("ping!")
            status = self.ping(5) # ping with timeout of 5 seconds

            # Call callback with status
            callback(status)

            time.sleep(1) # wait one second

    def start_heartbeat(self, callback):
        # Create the heartbeat threat and start it
        self.heartbeat_thread = threading.Thread(target = self.heartbeat, args=(callback,))
        self.heartbeat_thread.start()
