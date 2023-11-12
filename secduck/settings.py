"""Default Settings"""
import pyaudio

# Hardware Config
MODE_BUTTON = 4
CAPTURE_BUTTON = 14

# Audio Config
REC_CONFIG = {
    "nchannels": 1,
    "rate": 44100,
    "chunk": 1024,
    "sfmt": pyaudio.paInt16,
}

SPK_CONFIG = {
    "nchannels": 1,
    "rate": 44100 * 2,
    "chunk": 1024,
    "sfmt": pyaudio.paInt16,
}

# Server Config


# User Preferences
