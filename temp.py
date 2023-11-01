import asyncio
from gpiozero import Button
import time

button = Button(4, pull_up=True)

async def task():
    print("Async task started")
    await asyncio.sleep(1)
    print("Async task finished")

def button_pressed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(task())
    loop.close()

button.when_pressed = button_pressed

try:
    while True:
        pass
except KeyboardInterrupt:
    pass

