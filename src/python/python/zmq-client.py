import sys
import zmq
import threading
import time
import random

def subscriber_client():
    port = "5556"
    if len(sys.argv) > 1:
        port = sys.argv[1]
        int(port)

    if len(sys.argv) > 2:
        port1 = sys.argv[2]
        int(port1)

    # Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print("Collecting updates from weather server...")
    socket.connect("tcp://localhost:%s" % port)

    if len(sys.argv) > 2:
        socket.connect("tcp://localhost:%s" % port1)

    # Subscribe to zipcode, default is NYC, 10001
    topicfilter = "10001"
    # socket.setsockopt(zmq.SUBSCRIBE, topicfilter.encode())
    socket.setsockopt(zmq.SUBSCRIBE, "".encode())

    while(True):
        string = socket.recv().decode()
        topic, messagedata = string.split()
        print(f"{topic}, {messagedata}")

def publisher_server():
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)

    while True:
        topic = random.randrange(9999,10005)
        messagedata = random.randrange(1,215) - 80
        message = f"{topic} {messagedata}"
        print(message)
        socket.send(message.encode())
        time.sleep(1)
def rep_server():
    print("a")
    context = zmq.Context()
    print("a")
    socket = context.socket(zmq.REP)
    print("a")
    socket.bind("tcp://*:5555")
    print("Waiting for req message")

    while True:
        message = socket.recv_string()
        print(f"Received {message}")
        socket.send_string(f"Received: {message}")



t1 = threading.Thread(target=publisher_server)
t2 = threading.Thread(target=rep_server)

t1.start()
t2.start()