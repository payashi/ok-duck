import logging
from io import BytesIO
from typing import Optional
from os import path, system
from datetime import datetime

import base64
import requests
from requests.exceptions import RequestException

logger = logging.getLogger("Connector")

ALL_PROMPT_IDS = [
    "pause",
    "break",
    "focus",
    "wakeup",
    "exit",
    "review",
]
X_DIC = "/var/lib/mecab/dic/open-jtalk/naist-jdic"
M_VOICE = "/usr/share/hts-voice/mei_normal.htsvoice"

PROMPTS_PATH = path.join(path.dirname(__file__), "..", "prompts")


class Connector:
    """
    Connector class to fetch audio from server
    """

    def __init__(self, server_url: str):
        self.server_url = server_url
        self.user_id = "zsSs1w8tV3hMdniTt66uaDKC1i33"
        self.duck_id = "rpi-duck"
        self.prompt_texts = dict()

    def fetch(self, prompt_id: str) -> Optional[BytesIO]:
        """Fetch audio from server"""
        file_path = path.join(PROMPTS_PATH, f"{prompt_id}.wav")

        # Fetch from server if the file doesn't exist on local
        if path.exists(file_path) is False:
            self.sync(prompt_ids=[prompt_id])
        self.log_prompt(prompt_id)

        try:
            with open(file_path, "rb") as f:
                audio = BytesIO(f.read())
            return audio
        except FileNotFoundError:
            logger.info("File %s not found", f"prompts/{prompt_id}.wav")

    def sync(self, prompt_ids: Optional[list[str]] = None):
        """Sync audio from server"""
        if prompt_ids is None:
            prompt_ids = ALL_PROMPT_IDS

        data = {
            "user_id": self.user_id,
            "duck_id": self.duck_id,
            "prompt_ids": prompt_ids,
        }

        try:
            response = requests.post(
                f"{self.server_url}/sync",
                headers={"Content-Type": "application/json"},
                json=data,
                timeout=60,
            )
            response.raise_for_status()
            for prompt_id in prompt_ids:
                prompt = response.json()[prompt_id]
                text: str = prompt["text"]
                self.synthesize(prompt_id, text)
                self.prompt_texts[prompt_id] = text

                logger.info("Synced %s", prompt_id)

        except RequestException as e:
            logger.exception("Failed to request: %s", e.response)

    def log_prompt(self, prompt_id: str):
        """Log to server"""
        data = {
            "user_id": self.user_id,
            "duck_id": self.duck_id,
            "text": self.prompt_texts[prompt_id],
            "created_at": datetime.now().timestamp(),
        }
        logger.info("Send prompt log(%s) to server", prompt_id)
        try:
            response = requests.post(
                f"{self.server_url}/log/prompt",
                headers={"Content-Type": "application/json"},
                json=data,
                timeout=60,
            )
            response.raise_for_status()

        except RequestException as e:
            logger.exception("Failed to request: %s", e.response)
            return

    def log_record(self, audio: bytes):
        """Log to server"""
        data = {
            "user_id": self.user_id,
            "duck_id": self.duck_id,
            "created_at": datetime.now().timestamp(),
            "audio": self.marshal(audio),
        }
        logger.info("Send record log to server")
        try:
            response = requests.post(
                f"{self.server_url}/log/record",
                headers={"Content-Type": "application/json"},
                json=data,
                timeout=60,
            )
            response.raise_for_status()

        except RequestException as e:
            logger.exception("Failed to request: %s", e.response)
            return

    def synthesize(self, prompt_id: str, text: str, speed: float = 1.15):
        """Synthesize text to audio"""
        system(
            f"echo {text} | open_jtalk -x {X_DIC} -m {M_VOICE} -r {speed} -ow {path.join(PROMPTS_PATH, f'{prompt_id}.wav')}"
        )

    def marshal(self, data: bytes) -> str:
        """Convert bytes to base64 string"""
        return base64.b64encode(data).decode("utf-8")

    def unmarshal(self, data: str) -> bytes:
        """Convert base64 string to bytes"""
        return base64.b64decode(data.encode("utf-8"))
