from gpiozero import Button
from signal import pause

# GPIO4 - Button - GND
BUTTON_A = 4
BUTTON_B = 14

Button.was_held = False

btn_a = Button(BUTTON_A, pull_up=True)
btn_b = Button(BUTTON_B, pull_up=True)

def held(btn):
    btn.was_held = True
    print(btn.pin.number, "long hold")

def released(btn):
    if not btn.was_held:
        print(btn.pin.number, "short press")
    btn.was_held = False

btn_a.when_held = held
btn_a.when_released = released
btn_b.when_held = held
btn_b.when_released = released

pause()
