"""Abstract Duck with threading"""
import logging
import base64
from enum import Enum
from io import BytesIO
import requests
from requests.exceptions import RequestException
from .recorder import Recorder
from .speaker import Speaker
from .settings import REC_CONFIG, SPK_CONFIG


class DuckState(Enum):
    """States Duck can take"""

    INIT = 0
    PAUSE = 1
    FOCUS = 2
    BREAK = 3
    BUSY = 4


class Duck:
    """Duck which can be run either on a laptop or on a Raspberry Pi"""

    def __init__(
        self, user_id, duck_id, server_uri,
    ):
        self.user_id = user_id
        self.duck_id = duck_id
        self.server_uri = server_uri

        self.state = DuckState.INIT

        self.recorder = Recorder(**REC_CONFIG)
        self.speaker = Speaker(**SPK_CONFIG)

    def wake_up(self):
        """Sync user data with a server"""
        if self.state != DuckState.INIT:
            logging.error("DUCK: Cannot wake up from %s state.", self.state)
        logging.info("Duck: Synchronized user data with a server")
        self.state = DuckState.PAUSE
        self._quack()

    def _quack(self):
        """Say `Quack!`"""
        self.speaker.start("audio/quack.wav", 1.0)

    def on_focus(self):
        """Mention the start of the work"""
        params = {"user_id": self.user_id, "duck_id": self.duck_id}
        try:
            response = requests.get(
                f"{self.server_uri}/start_work", params=params, timeout=10
            )
            response.raise_for_status()
            logging.info("DUCK: Receive from server: %s", str(response.json()["text"]))
            audio = BytesIO(self._unmarshal(response.json()["audio"]))
            self.speaker.start(audio, 1.0)

        except RequestException as e:
            logging.exception("DUCK: Failed to request: %s", e.response)

    def on_pause(self):
        """Mention the pause of the work"""
        params = {"user_id": self.user_id, "duck_id": self.duck_id}
        try:
            response = requests.get(
                f"{self.server_uri}/start_pause", params=params, timeout=10
            )
            response.raise_for_status()
            logging.info("DUCK: Receive from server: %s", str(response.json()["text"]))
            audio = BytesIO(self._unmarshal(response.json()["audio"]))
            self.speaker.start(audio, 1.0)

        except RequestException as e:
            logging.exception("DUCK: Failed to request: %s", e.response)

    def on_break(self):
        pass

    def on_review(self):
        """Mention the start of the review"""
        # if self.state == DuckState.
        self.state = DuckState.BUSY
        params = {"user_id": self.user_id, "duck_id": self.duck_id}
        try:
            response = requests.get(
                f"{self.server_uri}/start_review", params=params, timeout=10
            )
            response.raise_for_status()
            logging.info("DUCK: Receive from server: %s", str(response.json()["text"]))
            audio = BytesIO(self._unmarshal(response.json()["audio"]))
            self.speaker.start(audio, 1.0)

        except RequestException as e:
            logging.exception("DUCK: Failed to request: %s", e.response)

        self.state = DuckState.PAUSE

    def start_recording(self):
        """Start listening to the mic"""
        logging.info("DUCK: Start listening to your voice")
        self.recorder.start()

    def stop_recording(self):
        """Stop listening to the mic"""
        logging.info("DUCK: Stop listening to your voice")
        self.recorder.stop()
        self._send_audio(self.recorder.get_wav())

    def _send_audio(self, audio: bytes):
        data = {
            "user_id": self.user_id,
            "duck_id": self.duck_id,
            "audio": self._marshal(audio),
        }

        try:
            response = requests.post(self.server_uri, json=data, timeout=10)
            response.raise_for_status()
            logging.info("DUCK: Receive from server: %s", str(response.text))
        except RequestException as e:
            logging.exception("DUCK: Failed to request: %s", e.response)

    def on_exit(self):
        pass
