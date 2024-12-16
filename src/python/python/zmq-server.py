import zmq
import random
import time
import threading

def sub_client():
    print("starting thread")
    port = "5556"

    # Socket to talk to server
    context2 = zmq.Context()
    socket2 = context2.socket(zmq.SUB)

    print("Collecting updates from weather server...")
    socket2.connect("tcp://localhost:%s" % port)
    socket2.setsockopt(zmq.SUBSCRIBE, "".encode())
    while True:

        string = socket2.recv().decode()
        topic, messagedata = string.split()
        text = f"{topic}, {messagedata}"
        print(text)

def req_client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5555")

    for i in range(5):
        print("Sending package")
        socket.send_string(f"Message {i}")
        print("Package send waiting for reply")
        reply = socket.recv_string()
        print(f"Reply: {reply}")
        time.sleep(5)



t1 = threading.Thread(target=sub_client)
t2 = threading.Thread(target=req_client)
t1.start()
t2.start()