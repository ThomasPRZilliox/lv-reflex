"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import zmq
import time
from datetime import datetime
import threading
import asyncio


from rxconfig import config


class State(rx.State):
    """The app state."""
    count: int = 0
    show_progress: bool = False
    text_indicator: str = "Waiting for server..."
    text_rep:str = ""

    @rx.event(background=True)
    async def query_server(self):
            print("starting query server")
            async with self:
                self.text_rep = "starting query server"
            context = zmq.Context()
            print("creating query socket")
            async with self:
                self.text_rep = "creating query socket"
            socket = context.socket(zmq.REQ)
            print("connection to query socket")
            async with self:
                self.text_rep = "connection to query socket"
            socket.connect("tcp://127.0.0.1:5555")
            print("Socket connected !")
            async with self:
              self.text_rep = "Socket connected !"

            for i in range(5):
                async with self:
                    payload_to_send = f"Message {i}"
                    print(f"sendind socket: {payload_to_send} ")
                    socket.send_string(payload_to_send)
                    print("Package send, waiting for reply...")
                    reply = socket.recv_string()
                    text = f"Reply: {reply}"
                    print(text)
                    self.text_rep = text
                    time.sleep(1)

    current_time: str = "Fetching time..."

    @rx.event(background=True)
    async def sub_to_event(self):
        print("starting thread")
        port = "5556"

        # Socket to talk to server
        context2 = zmq.Context()
        socket2 = context2.socket(zmq.SUB)

        print("Collecting updates from weather server...")
        socket2.connect("tcp://localhost:%s" % port)
        socket2.setsockopt(zmq.SUBSCRIBE, "".encode())
        while True:
            async with self:
                string = socket2.recv().decode()
                topic, messagedata = string.split()
                text = f"{topic}, {messagedata}"
                print(text)
                self.text_indicator = text





@rx.page(on_load=State.sub_to_event)
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Let's debug 0MQ !", size="9"),
            # rx.text(
            #     "Get started by editing ",
            #     rx.code(f"{config.app_name}/{config.app_name}.py"),
            #     size="5",
            # ),
            rx.button(
                "Query server",
                color_scheme="red",
                on_click=State.query_server,
                # on_click=State.query_server,
            ),
            rx.text(f"Request from the request: {State.text_rep} "),
            rx.text(f"Value from the subscription: {State.text_indicator} "),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)
