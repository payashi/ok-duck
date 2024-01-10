"""Program which can be executed on a Raspberry Pi"""

from signal import pause
from secduck import DeviceInput, DeviceOutput, Connector, Speaker, Recorder, Duck

SERVER_URL = "https://secduck-upload-server-xwufhlvadq-an.a.run.app"


device_input = DeviceInput()
device_output = DeviceOutput()
connector = Connector(SERVER_URL)
speaker = Speaker()
recorder = Recorder()
duck = Duck(device_input, device_output, connector, speaker, recorder)


try:
    duck.on_wakeup()

    pause()

finally:
    print('Shutting down...')
