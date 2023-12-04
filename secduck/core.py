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

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d:%(threadName)s:%(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


class DuckState(Enum):
    """States Duck can take"""

    INIT = 0
    PAUSE = 1
    WORK = 2
    BREAK = 3
    BUSY = 4


class Duck:
    """Duck which can be run either on a laptop or on a Raspberry Pi"""

    def __init__(self, user_id, duck_id, server_uri, audio_volume: float = 1.0):
        self.user_id = user_id
        self.duck_id = duck_id
        self.server_uri = server_uri
        self.audio_volume = audio_volume

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
        self.speaker.start("audio/quack.wav", self.audio_volume)

    def detect_long_press(self): # long push
        """Switch its `state` and speak accordingly"""
        if self.state in [DuckState.PAUSE, DuckState.WORK]:
            # Start Break
            self.state = DuckState.BUSY
            self.start_break()
            self.state = DuckState.BREAK

        elif self.state == DuckState.BREAK:
            # Start Work
            self.state = DuckState.BUSY
            self.start_work()
            self.state = DuckState.WORK
        else:
            logging.error("DUCK: cannot switch state while %s", self.state)

    def detect_short_press(self):
        """Switch its `state` and speak accordingly"""
        if self.state in [DuckState.BREAK, DuckState.WORK]:
            # Start Pause
            self.state = DuckState.BUSY
            self.start_pause()
            self.state = DuckState.PAUSE

        elif self.state == DuckState.PAUSE:
            # Start Work
            self.state = DuckState.BUSY
            self.start_work()
            self.state = DuckState.WORK
        else:
            logging.error("DUCK: cannot switch state while %s", self.state)

    def detect_power_off(self):
        '''Start security review and shut it down after confirmation prompt'''
        # Prompt for serurity review
        # Detect end of the talking from a user
        # Confirm if it is ok to shut down
        # detect power_off button again
        # call(["sudo", "shutdown", "-h", "now"])

    def start_work(self):
        """Mention the start of the work"""
        params = {"user_id": self.user_id, "duck_id": self.duck_id}
        try:
            response = requests.get(
                f"{self.server_uri}/start_work", params=params, timeout=10
            )
            response.raise_for_status()
            logging.info("DUCK: Receive from server: %s", str(response.json()["text"]))
            audio = BytesIO(self._unmarshal(response.json()["audio"]))
            self.speaker.start(audio, self.audio_volume)

        except RequestException as e:
            logging.exception("DUCK: Failed to request: %s", e.response)

    def start_pause(self):
        """Mention the pause of the work"""
        params = {"user_id": self.user_id, "duck_id": self.duck_id}
        try:
            response = requests.get(
                f"{self.server_uri}/start_pause", params=params, timeout=10
            )
            response.raise_for_status()
            logging.info("DUCK: Receive from server: %s", str(response.json()["text"]))
            audio = BytesIO(self._unmarshal(response.json()["audio"]))
            self.speaker.start(audio, self.audio_volume)

        except RequestException as e:
            logging.exception("DUCK: Failed to request: %s", e.response)

    def start_break(self):
        pass

    def start_review(self):
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
            self.speaker.start(audio, self.audio_volume)

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

    def _marshal(self, data: bytes) -> str:
        return base64.b64encode(data).decode("utf-8")

    def _unmarshal(self, data: str) -> bytes:
        return base64.b64decode(data.encode("utf-8"))
