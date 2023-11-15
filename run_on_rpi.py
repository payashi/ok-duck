"""Program which can be executed on a Raspberry Pi"""

import pathlib
from signal import pause
from gpiozero import Button

from secduck import LaptopDuck

SERVER_URI = "https://secduck-upload-server-xwufhlvadq-an.a.run.app"
AUDIO_PATH = pathlib.Path(__file__).parent.joinpath("audio/sstar.wav")

duck = LaptopDuck("payashi", SERVER_URI)

Button.was_held = False
btn_a = Button(4, pull_up=True)
btn_b = Button(14, pull_up=True)

btn_a.when_pressed = duck.start_recording
btn_a.when_released = duck.stop_recording


def long_press(button):
    button.was_held = True
    print("long press")
    duck.stop_speaking()


def short_press(button):
    if not button.was_held:
        print("short press")
        duck.start_speaking(str(AUDIO_PATH))
    button.was_held = False


btn_b.when_held = long_press
btn_b.when_released = short_press

pause()
