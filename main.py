from secduck import ModeButton, CaptureButton, Duck
import asyncio
from signal import pause

duck = Duck("payashi")

# asyncio.get_event_loop().run_until_complete(duck.boot())

# cbtn = CaptureButton(14, pull_up=True)

def long_cb():
    print("long")
    print(duck.state)
    duck.to_break()
    print(duck.state)

def short_cb():
    print("short")
    print(duck.state)
    duck.to_pause()
    print(duck.state)

mbtn = ModeButton(4, pull_up=True, long_callback=long_cb, short_callback=short_cb)

duck.boot()

pause()
