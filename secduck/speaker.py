"""Speaker class"""
import logging
import wave
import threading
import pyaudio


class Speaker:
    """Audio Speaker"""

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

        self._audio = pyaudio.PyAudio()

        self._running = False

    def start(self, file: str):
        """Start playing sound"""
        if self._running:
            logging.warning("Speaker is already running")
            self.stop()
        self._running = True

        t = threading.Thread(
            target=self._play,
            args=(file,),
            daemon=True,
        )
        t.start()

    def stop(self):
        """Stop playing sound"""
        if not self._running:
            logging.warning("Speaker is already stopped")
            return
        self._running = False

    def _play(self, file: str):
        """Play an audio `file`"""
        stream = self._audio.open(
            format=self.sfmt,
            channels=self.nchannels,
            rate=self.rate,
            output=True,
            frames_per_buffer=self.chunk,
        )
        wf = wave.open(file, "rb")
        data = wf.readframes(self.chunk)
        while data != "" and self._running:
            stream.write(data)
            data = wf.readframes(self.chunk)
