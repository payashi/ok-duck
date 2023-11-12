import wave
import pyaudio
import threading
from gpiozero import Button

from .settings import CHANNELS, RATE, FORMAT, CHUNK


class CaptureButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.frames = []
        self.audio = pyaudio.PyAudio()

        self.when_pressed = self._pressed
        self.when_released = self._released

    def _pressed(self):
        print("Recording started...")

        self.frames = []

        stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        while self.is_pressed:
            self.frames.append(stream.read(CHUNK))
        stream.stop_stream()
        stream.close()

        print("Recording stopped.")

    def _released(self):
        # TODO: send audio data to a server via WebSocket API
        wf = wave.open("captured.wav", "wb")
        wf.setnchannels(CHANNELS)
        wf.setframerate(RATE)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.writeframes(b"".join(self.frames))
        wf.close()
        print("Audio was saved")
