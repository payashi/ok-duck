from gpiozero import Button

# GPIO4 - Button - GND
BUTTON_PIN = 4

button = Button(BUTTON_PIN, pull_up=True)

try:
    while True:
        button.wait_for_press()
        print("Processing something...")

        button.wait_for_release()
        print("The process has ended")

except KeyboardInterrupt:
    print("\nProgram terminated")
