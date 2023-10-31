from secduck import ModeButton, CaptureButton
import threading
from signal import pause

cbtn = CaptureButton(14, pull_up=True)

def long_cb():
    print("long")

def short_cb():
    print("short")

mbtn = ModeButton(4, pull_up=True, long_callback=long_cb, short_callback=short_cb)


pause()
