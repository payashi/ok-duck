"""Recorder class"""
import threading
import logging
import wave
from io import BytesIO
import pyaudio

logger = logging.getLogger('Recorder')

class Recorder:
    """Audio Recorder"""

    def __init__(
        self,
        nchannels: int = 1,
        rate: int = 44100,
        sfmt: int = pyaudio.paInt16,
        chunk: int = 1024,
    ):
        self.nchannels = nchannels
        self.rate = rate
        self.sfmt = sfmt  # sample format
        self.chunk = chunk

        self.frames = []
        self._audio = pyaudio.PyAudio()

        self._running = False

    def start(self):
        """Start recording"""
        logger.info('Start recording')
        if self._running:
            logger.warning("Already running")
            return
        self._running = True

        t = threading.Thread(target=self._record, daemon=True)
        t.start()

    def stop(self):
        """Stop recording"""
        logger.info('Stop recording')
        if not self._running:
            logging.warning("Already stopped")
            return
        self._running = False

    def _record(self):
        """Record while `_running` is True"""
        stream = self._audio.open(
            format=self.sfmt,
            channels=self.nchannels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )
        self.frames = []
        while self._running:
            self.frames.append(stream.read(self.chunk))

        stream.stop_stream()
        stream.close()

    def export(self) -> bytes:
        """Export recorded data as BytesIO"""
        file = BytesIO()
        wf = wave.open(file, "wb")
        wf.setnchannels(self.nchannels)
        wf.setframerate(self.rate)
        wf.setsampwidth(self._audio.get_sample_size(self.sfmt))
        wf.writeframes(b"".join(self.frames))
        wf.close()
        return file.getvalue()
