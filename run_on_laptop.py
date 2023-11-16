"""Program which can be executed on a laptop"""

import threading
from secduck import Duck

SERVER_URI = "http://localhost:8080"
# SERVER_URI = "https://secduck-upload-server-xwufhlvadq-an.a.run.app"

duck = Duck("payashi", "laptop-duck", SERVER_URI, 1.0)

duck.wake_up()


def key_detect():
    """Detect a key to press"""
    while True:
        val = input()
        if val == "start recording":
            duck.start_recording()
        elif val == "stop recording":
            duck.stop_recording()
        elif val == "short push":
            duck.detect_mode_switch()
        elif val == "long push":
            duck.start_review()


gpio_thread = threading.Thread(target=key_detect)

gpio_thread.start()
