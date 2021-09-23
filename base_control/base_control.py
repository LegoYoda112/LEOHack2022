import zmq

class SatConnection:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port

class BaseControl:
    def __init__(self, name):
        self.name = name

        self.sat = None

        self.context = zmq.Context()

    def connect_socket(self, ip, port):
        self.send_socket = self.context.socket(zmq.REQ)
        self.send_socket.setsockopt(zmq.LINGER, 0)
        self.send_socket.connect("tcp://{}:{}".format(ip, port))
    
    def send_msg(self, msg_data):
        self.send_socket.send_string(msg_data)
    
    def connect_sat(self, ip, port, timeout = 1):
        self.connect_socket(ip, port)
        self.send_msg("hello!")

        
        poller = zmq.Poller()
        poller.register(self.send_socket, zmq.POLLIN)

        events = poller.poll(timeout * 1000)

        print(len(events))

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

        def ping(self):
            self.send_msg("ping")

            poller = zmq.Poller()
            poller.register(self.send_socket, zmq.POLLIN)

            events = poller.poll(timeout * 1000)

            print(len(events))

            if(len(events) == 0):
                print("Connection Failed")