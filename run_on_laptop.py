"""Program which can be executed on a laptop"""

import threading
import pathlib
from secduck import LaptopDuck

SERVER_URI = "http://localhost:8080"
# SERVER_URI = "https://secduck-upload-server-xwufhlvadq-an.a.run.app"

AUDIO_PATH = pathlib.Path(__file__).parent.joinpath("audio/sstar.wav")

duck = LaptopDuck("payashi", SERVER_URI)


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
