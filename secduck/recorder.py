"""Recorder class"""
import threading
import logging
import pyaudio
import wave

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d:%(threadName)s:%(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


class Recorder:
    """Audio Recorder"""

    def __init__(
        self,
        nchannels: int,
        rate: int,
        sfmt: int,
        chunk: int,
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
        if self._running:
            logging.warning("Recorder is already running")
            return
        self._running = True

        t = threading.Thread(target=self._record, daemon=True)
        t.start()

    def stop(self):
        """Stop recording"""
        if not self._running:
            logging.warning("Recorder is already stopped")
            return
        self._running = False

        self._save()

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

    def _save(self):
        """Save `frames` as captured.wav file"""
        # TODO: send audio data to a server via WebSocket API
        wf = wave.open("captured.wav", "wb")
        wf.setnchannels(self.nchannels)
        wf.setframerate(self.rate)
        wf.setsampwidth(self._audio.get_sample_size(self.sfmt))
        wf.writeframes(b"".join(self.frames))
        wf.close()
