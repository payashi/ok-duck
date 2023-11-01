import asyncio
import time
import threading
from gpiozero import Button
from transitions.extensions.asyncio import AsyncMachine
from transitions import Machine

from .settings import CAPTURE_BUTTON, MODE_BUTTON
from .capture_button import CaptureButton
from .mode_button import ModeButton

class Duck(object):
    states = ["init", "pause", "break", "work"]

    def __init__(self, user_id):
        self.user_id = user_id
        self.loop = asyncio.new_event_loop()

        boot = dict(
            trigger="boot",
            source="init",
            dest="pause",
            before="sync",
        )

        temp = dict(
            trigger="temp",
            source="*",
            dest="work",
            before="greet",
        )

        self.machine = Machine(
            model=self,
            states=Duck.states,
            transitions=[boot, temp],
            initial="init",
        )

    def greet(self):
        print('hello!')

    def sync(self):
        # TODO: Get configurations from a server
        print("Getting configurations from the server")
        self.loop.run_until_complete(self.async_task())
        # TODO: quack!
        print("Quack!")

    async def async_task(self):
        print(self.state)
        await asyncio.sleep(1)


class AsyncDuck(object):
    states = ["init", "pause", "break", "work"]

    def __init__(self, user_id):
        self.user_id = user_id
        # t = threading.Thread(target=capture)
        # t.start()

        boot = dict(
            trigger="boot",
            source="init",
            dest="pause",
            before="sync",
        )

        temp = dict(
            trigger="temp",
            source="*",
            dest="work",
            before="greet",
        )

        self.machine = AsyncMachine(
            model=self,
            states=Duck.states,
            transitions=[boot, temp],
            initial="init",
        )

    async def greet(self):
        print('hello!')

    async def sync(self):
        # TODO: Get configurations from a server
        print("Getting configurations from the server")
        await asyncio.sleep(1)
        # TODO: quack!
        print("Quack!")
