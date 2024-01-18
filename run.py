"""Program which can be executed on a laptop"""

import logging
from signal import pause
from secduck import DeviceInput, DeviceOutput, Connector, Speaker, Recorder, Duck

# SERVER_URL = "https://secduck-upload-server-xwufhlvadq-an.a.run.app"
SERVER_URL = "http://localhost:8080"
IS_VIRTUAL = True

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname).4s - [%(name)s] %(message)s',
    datefmt='%H:%M:%S'
)

duck = Duck(
    device_input=DeviceInput(IS_VIRTUAL, spi=False),
    device_output=DeviceOutput(IS_VIRTUAL),
    connector=Connector(SERVER_URL),
    speaker=Speaker(),
    recorder=Recorder(),
)


try:
    duck.on_wakeup()
    pause()

finally:
    duck.on_exit()
    print('Shutting down...')
