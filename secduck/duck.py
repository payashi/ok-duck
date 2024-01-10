'''
A class that represents the Duck.
'''

from enum import Enum
import logging
import asyncio

from .recorder import Recorder
from .speaker import Speaker
from .device_input import DeviceInput
from .device_output import DeviceOutput
from .connector import Connector

logger = logging.getLogger('Duck')

class DuckState(Enum):
    """States Duck can take"""

    PAUSE = 1
    FOCUS = 2
    BREAK = 3
    BUSY = 4

class Duck:
    '''
    A class that represents the Duck.

    Args:
        device_input: DeviceInput
        device_output: DeviceOutput
        connector: Connector
        speaker: Speaker
        recorder: Recorder
    '''
    def __init__(
        self, device_input: DeviceInput, device_output: DeviceOutput,
        connector: Connector, speaker: Speaker, recorder: Recorder):
        self.device_input = device_input
        self.device_output = device_output
        self.connector = connector
        self.speaker = speaker
        self.recorder = recorder

        self.state = DuckState.PAUSE

        # Interaction mappings
        self.device_input.on_pause = self.on_pause
        self.device_input.on_break = self.on_break
        self.device_input.on_focus = self.on_focus
        self.device_input.on_start_recording = self.on_start_recording
        self.device_input.on_stop_recording = self.on_stop_recording
        self.device_input.on_review = self.on_review

    def on_pause(self):
        '''Duck starts pausing.'''
        logger.info("Start pausing")
        if self.state == DuckState.BUSY:
            logger.warning("Busy now")
            return
        self.state = DuckState.BUSY
        self.device_output.on_pause()
        audio = self.connector.send('pause')
        if audio:
            self.speaker.start(audio, self.device_input.volume)
        self.state = DuckState.PAUSE

    def on_break(self):
        '''Duck takes a break.'''
        logger.info("Take a break")
        if self.state == DuckState.BUSY:
            logger.warning("Busy now")
            return
        self.state = DuckState.BUSY
        self.device_output.on_break()
        audio = self.connector.send('break')
        if audio:
            self.speaker.start(audio, self.device_input.volume)
        self.state = DuckState.BREAK

        asyncio.run(self.reserve(5*60, self.on_focus))

    def on_focus(self):
        '''Duck starts focusing.'''
        logger.info("Start focusing")
        if self.state == DuckState.BUSY:
            logger.warning("Busy now")
            return
        self.state = DuckState.BUSY
        self.device_output.on_focus()
        audio = self.connector.send('focus')
        if audio:
            self.speaker.start(audio, self.device_input.volume)
        self.state = DuckState.FOCUS

        asyncio.run(self.reserve(25*60, self.on_focus))

    def on_review(self):
        '''Duck starts reviewing.'''
        logger.info("Start reviewing")
        if self.state == DuckState.BUSY:
            logger.warning("Busy now")
            return
        self.state = DuckState.BUSY
        self.device_output.on_review()
        audio = self.connector.send('review')
        if audio:
            self.speaker.start(audio, self.device_input.volume)
        self.state = DuckState.PAUSE

    def on_start_recording(self):
        '''Duck starts recording.'''
        logger.info("Start recording")
        self.recorder.start()

    def on_stop_recording(self):
        '''Duck stops recording.'''
        logger.info("Stop recording")
        self.recorder.stop()
        audio = self.recorder.export()
        with open("out.wav", "wb") as outfile:
            outfile.write(audio.getbuffer())

    def on_wakeup(self):
        '''Duck wakes up.'''
        logger.info("Wake up")
        if self.state == DuckState.BUSY:
            logger.warning("Busy now")
            return
        audio = self.connector.send('wakeup')
        if audio:
            self.speaker.start(audio, self.device_input.volume)

    def on_exit(self):
        '''Duck exits.'''
        logger.info("Exit")
        if self.state == DuckState.BUSY:
            logger.warning("Busy now")
            return
        audio = self.connector.send('exit')
        if audio:
            self.speaker.start(audio, self.device_input.volume)

    async def reserve(self, duration: int, callback):
        '''Callback after duration.'''
        await asyncio.sleep(duration)
        callback()
