import zmq
import threading
import time

import serial

import logging

from sat_controller import SatControllerInterface

class SatComms:
    def __init__(self, name, serial_name):
        # Init ZMQ socket
        self.sock = zmq.Context().socket(zmq.REP)
        self.sock.bind("tcp://0.0.0.0:9000")

        # Assign sat name
        self.name = name
        
        # Place holder for serial
        self.ser = None

        # Variable to store if we have just disconnected
        self.lost_connection = False

        self.logger = logging.getLogger(__name__)

    def start(self):

        # Set up serial port and connect
        self.ser = serial.Serial(serial_name, 115200, write_timeout = 0.001)

        # Create the comms thread
        self.thread = threading.Thread(target= self.comms_thread, args = ())
        self.thread.setDaemon(True)

        # Start the comms thread
        self.thread.start()

        # Loop until the user presses Ctrl+C
        # TODO: Add a way to remotely stop all threads, daemon somewhat fixes this
        while True:
            time.sleep(1)

        thread.join()

    # Coms thread to handle receiving and responding to base station messages
    def comms_thread(self):
        while True:

            # Register a poller to revice messages
            poller = zmq.Poller()
            poller.register(self.sock, zmq.POLLIN)

            events = poller.poll(timeout = 2000)

            if(len(events) > 0):
                # Set lost connection back to false
                self.lost_connection = False

                # Decode received message
                message = events[0][0].recv().decode("utf-8")

                # Split into command and args
                split_message = message.split(" ")

                self.logger.debug(split_message)

                response = "default"
                
                # Switch based on command
                if split_message[0] == "HB":
                    response = self.receive_heartbeat(split_message[1])
                elif split_message[0] == "INIT":
                    response = self.receive_INIT(split_message[1])
                elif split_message[0] == "RUN":
                    response = self.receive_RUN(split_message[1:])
                
                # Send a reply
                self.sock.send_string(response)
            else:
                self.logger.debug("No message received, resetting")

                # If lost connection is false, print warning
                # and set it to true
                if(self.lost_connection == False):
                    self.logger.warn("Lost connection to base station")
                    self.lost_connection = True

                # Reset connection info
                self.reset()
    
    # When a heartbeat is received
    def receive_heartbeat(self, message):
        self.logger.debug("Received HB: " + message)
        return self.name

    # If an INIT message is received
    def receive_INIT(self, message):
        self.logger.debug("Received INIT: " + message)

        self.logger.info("Connected to base_station")

        return "ACK " + str(self.name)

    # If a DRIVE message is received
    def receive_RUN(self, message):
        self.logger.debug("Received RUN: ")

        twist_msg = message.thrust
        time_step = message.time_step

        self.write_impulse(twist_msg, time_step)
        return "ACK " + return_msg

    # Writes a force to the sat, returns current position
    # Note this is technically an impulse,
    # as it will only be applied for the next update
    def write_impulse(self, twist_msg, time_step):
        self.logger.debug("Writing twist")
        xs = twist_msg.f_x * time_step
        ys= twist_msg.f_y * time_step
        taus = twist_msg.tau * time_step

        
        sendString = "twist %.2f %.2f %.2f\n" % (xs, ys, taus)

        # Flush input, output, then send string
        try:
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(bytes(sendString, "utf-8"))
        except Exception as e:
            print(e)

    # Writes an absolute position update to the sat
    def write_pos_update(self, pose_msg):
        self.logger.debug("Writing pos update")
        x = pose_msg.x
        y = pose_msg.y
        theta = pose_msg.theta

        # Position update string
        sendString = "pos %.2f %.2f %.2f\n" % (x, y, theta)

        # Flush input, output, then send string
        try:
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(bytes(sendString, "utf-8"))
        except Exception as e:
            print(e)

    # Write a reset message to the sat
    def write_reset(self):
        self.logger.debug("Writing pos update")

        # Flush input, output, then send string
        try:
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(bytes("reset", "utf-8"))
        except Exception as e:
            print(e)

    # Sat reset (either called, or if comms is lost)
    def reset(self):
        self.logger.debug("Resetting")
        self.write_twist(0, 0, 0)
        self.reset_callback()
