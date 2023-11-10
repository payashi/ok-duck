"""Playground"""

import threading
import pathlib
from secduck import LaptopDuck


duck = LaptopDuck("payashi", "server")
AUDIO_PATH = pathlib.Path(__file__).parent.joinpath("sample.wav")


def key_detect():
    """Detect a key to press"""
    while True:
        val = input()
        if val == "start recording":
            duck.start_recording()
        elif val == "stop recording":
            duck.stop_recording()
        elif val == "start speaking":
            duck.start_speaking(str(AUDIO_PATH))
        elif val == "stop speaking":
            duck.stop_speaking()


gpio_thread = threading.Thread(target=key_detect)

gpio_thread.start()
