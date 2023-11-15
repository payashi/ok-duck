"""Speaker class"""
import logging
import wave
import threading
import numpy as np

import pyaudio


class Speaker:
    """Audio Speaker"""

    def __init__(self, chunk: int):
        self.chunk = chunk

        self._running = False
        self._thread = None

        self._audio = pyaudio.PyAudio()

    def start(self, file: str):
        """Start playing sound"""
        if self._running or self._thread is not None:
            logging.warning("Speaker is already running")
            self.stop()
        self._running = True

        self._thread = threading.Thread(
            target=self._play,
            args=(file,),
            daemon=True,
        )
        self._thread.start()

    def stop(self):
        """Stop playing sound"""
        if not self._running or self._thread is None:
            logging.warning("Speaker is already stopped")
            return
        self._running = False
        self._thread.join()
        self._thread = None

    def _play(self, file: str, volume: float = 1.0):
        """Play an audio `file`"""

        wf = wave.open(file, "rb")

        stream = self._audio.open(
            format=self._audio.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
            frames_per_buffer=self.chunk,
        )

        audio_dtype = self._get_dtype(wf.getsampwidth())
        raw_bytes = wf.readframes(self.chunk)

        while raw_bytes != "" and self._running:
            raw_npdata = np.frombuffer(raw_bytes, dtype=audio_dtype)
            gained_npdata = raw_npdata * volume
            gained_bytes = gained_npdata.astype(audio_dtype).tobytes()

            stream.write(gained_bytes)
            raw_bytes = wf.readframes(self.chunk)

    def _get_dtype(self, sampwidth: int) -> type:
        if sampwidth == 2:
            return np.int16
        elif sampwidth == 4:
            return np.int32
        elif sampwidth == 8:
            return np.int64
