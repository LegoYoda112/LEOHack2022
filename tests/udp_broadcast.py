
import os
import socket
import sys
import time

import zmq

import threading

PING_PORT_NUMBER = 9998
data_port = 9999
PING_MSG_SIZE = 1
PING_INTERVAL = 1

def reply_thread():
    context = zmq.Context()
    reply_socket = context.socket(zmq.REP)
    reply_socket.bind("tcp://*:%s" % data_port)

    while True:
        print("Waiting for request")
        message = reply_socket.recv()
        print("Message received")
        reply_socket.send("Name!")

def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('', PING_PORT_NUMBER))

    poller = zmq.Poller()
    poller.register(sock, zmq.POLLIN)

    ping_at = time.time()

    # Data socket
    context = zmq.Context()

    while True:
        timeout = ping_at - time.time()
        if timeout < 0:
            timeout = 0

        print(timeout)

        try:
            events = dict(poller.poll( 1000 * timeout))
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            break

        if sock.fileno() in events:
            msg, addrinfo = sock.recvfrom(PING_MSG_SIZE)
            print("Found peer %s:%d" % addrinfo)
            print("Asking peer for name")

            # Reply socket
            data_socket = context.socket(zmq.REQ)
            data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
            data_socket.bind("tcp://%s:%d" % (addrinfo[0], data_port))

            data_socket.send_string("Hello")
            name = data_socket.recv()

            print("Name:", name)

        if time.time() >= ping_at:
            print("Pinging peers...")
            sock.sendto(b'!', 0, ("255.255.255.255", PING_PORT_NUMBER))
            ping_at = time.time() + PING_INTERVAL


if __name__ == '__main__':
    main_thread = threading.Thread(target = main)
    main_thread.start()

    reply_thread = threading.Thread(target = reply_thread)
    reply_thread.start()