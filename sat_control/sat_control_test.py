import zmq  # Server

sock = zmq.Context().socket(zmq.REP)
sock.bind("tcp://127.0.0.1:9000")

print(sock.recv())  # Prints "0"
sock.send_string('DAX')