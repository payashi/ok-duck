import asyncio
import time
import threading
from gpiozero import Button
from transitions.extensions.asyncio import AsyncMachine

from .settings import CAPTURE_BUTTON, MODE_BUTTON
from .capture_button import CaptureButton
from .mode_button import ModeButton


class Duck(object):
    states = ["init", "pause", "break", "work"]

    def __init__(self, user_id):
        self.user_id = user_id
        # t = threading.Thread(target=capture)
        # t.start()

        transition = dict(
            trigger="boot",
            source="init",
            dest="pause",
            before="sync",
        )

        self.machine = AsyncMachine(
            model=self,
            states=Duck.states,
            transitions=[transition],
            initial="init",
        )

    async def sync(self):
        # TODO: Get configurations from a server
        print("Getting configurations from the server")
        await asyncio.sleep(1)
        # TODO: quack!
        print("Quack!")

if __name__ == "__main__":
    duck = Duck("payashi")

    asyncio.get_event_loop().run_until_complete(duck.boot())

    def long_callback():
        print("long")

    def short_callback():
        print("short")
    
    cbtn = CaptureButton(CAPTURE_BUTTON, pull_up=True)
    mbtn = ModeButton(
        MODE_BUTTON, pull_up=True,
        long_callback=long_callback,
        short_callback=short_callback)

