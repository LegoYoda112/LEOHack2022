import zmq
import threading
import time

import serial

import logging

class SatComms:
    def __init__(self, name):
        # Init ZMQ socket
        self.sock = zmq.Context().socket(zmq.REP)
        self.sock.bind("tcp://0.0.0.0:9000")

        # Assign sat name
        self.name = name

        # Drive and Reset callback placeholder
        self.drive_callback = None
        self.reset_callback = None

        # Variable to store if we have just disconnected
        self.lost_connection = False

        self.logger = logging.getLogger(__name__)

    def register_drive_callback(self, callback):
        self.drive_callback = callback

    def register_reset_callback(self, callback):
        self.reset_callback = callback

    def start(self):

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
                elif split_message[0] == "DRIVE":
                    response = self.receive_DRIVE(split_message[1:])
                
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
    def receive_DRIVE(self, message):
        self.logger.debug("Received DRIVE: ")

        self.drive_callback(float(message[0]), float(message[1]), float(message[2]))

        return "ACK"

    # Sat reset (either called, or if comms is lost)
    def reset(self):
        self.logger.debug("Resetting")
        self.reset_callback()
