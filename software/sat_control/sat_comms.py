from operator import truediv
import threading
import time
import logging

import zmq

import serial

from sat_controller import sat_msgs

class SatComms:
    """ Class to handle sat communication and control """
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

        self.thread = None

        # Various frames
        self.odom_frame = sat_msgs.Pose2D
        self.sat_frame = sat_msgs.Pose2D
        self.offset_frame = sat_msgs.Pose2D

    def start(self):
        """ Starts the sat communication """
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

        # thread.join()

    # Coms thread to handle receiving and responding to base station messages
    def comms_thread(self):
        """ Communication thread """
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
        """Handle recived heartbeat message """ 
        self.logger.debug("Received HB: " + message)
        return self.name

    # If an INIT message is received
    def receive_init(self, message):
        """ Handle recived init message """ 
        self.logger.debug("Received INIT: " + message)

        self.logger.info("Connected to base_station")

        return "ACK " + str(self.name)

    # If a DRIVE message is received
    def receive_control(self, message):
        """ Handle control message """
        self.logger.debug("Received RUN: ")

        # Update odometry
        self.update_odom_frame()
        self.update_odom_offset(message.absolute_pose)

        twist_msg = message.thrust
        time_step = message.time_step

        
        return "ACK " + return_msg

    def cmd_vel_and_servo(self, cmd_vel, servo_states):
        """ Writes desired velocity and servo states """
        self.logger.debug("Writing vel and servo")
        
        sendString = "ctl %.2f %.2f %.2f" % (cmd_vel.x, cmd_vel.y, cmd_vel.omega)
        sendString += "%.2f %.2f %.2f\n" % (servo_states.servo1, servo_states.servo2, servo_states.servo3)

        # Flush input, output, then send string
        try:
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(bytes(sendString, "utf-8"))
        except Exception as e:
            print(e)

    def update_odom_frame(self):
        """ Updates odometry frame """
        try:
            # Requests odom frame
            self.ser.write(bytes("odom\n", "utf-8"))

            # Recives and parses the odometry frame
            odom_frame = self.ser.readline()
            odom_frame = odom_frame.split(" ")
            odom_frame = [float(num) for num in odom_frame]

            self.odom_frame.x = odom_frame[0]
            self.odom_frame.y = odom_frame[1]
            self.odom_frame.theta = odom_frame[2]
        except Exception as e:
            print(e)

    # Updates odometry offset
    def update_odom_offset(self, absolute_pose):
        """ Updates the odometry offset """

        # If sat not read correctly, do not update offset
        if(not absolute_pose.x < 1000):
            # For IIR filtering
            # Over time, position will converge to absolut readings
            # But short term is goverend by odometry
            linear_filter_const = 0.5
            angular_filter_const = 0.5

            self.offset_frame.x += (self.odom_frame.x - absolute_pose.x + self.offset_frame.x) * linear_filter_const
            self.offset_frame.y += (self.odom_frame.x - absolute_pose.y + self.offset_frame.y) * linear_filter_const
            self.offset_frame.theta += (self.odom_frame.theta - absolute_pose.theta + self.offset_frame.theta) * angular_filter_const
        
        # Update sat frame
        self.sat_frame.x = self.odom_frame.x + self.offset_frame.x
        self.sat_frame.y = self.odom_frame.y + self.offset_frame.y
        self.sat_frame.theta = self.odom_frame.theta + self.offset_frame.theta

    # Write a reset message to the sat
    def write_reset(self):
        """Write a reset message to the sat"""
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
