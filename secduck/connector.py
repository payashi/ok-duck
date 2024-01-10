from io import BytesIO
from typing import Union, Optional

import base64
import requests
from requests.exceptions import RequestException

class Connector:
    def __init__(self, server_url: str):
        self.server_url = server_url
        # TODO: Fetch user_id and duck_id from the server
        self.user_id = 'payashi'
        self.duck_id = 'rpi-duck'

    def send(self, path: str) -> Optional[BytesIO]:
        return None


    def marshal(self, data: bytes) -> str:
        '''
        Convert bytes to base64 string
        '''
        return base64.b64encode(data).decode("utf-8")

    def unmarshal(self, data: str) -> bytes:
        '''
        Convert base64 string to bytes
        '''
        return base64.b64decode(data.encode("utf-8"))