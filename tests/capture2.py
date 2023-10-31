import pyaudio
import wave

audio = pyaudio.PyAudio()
frames = []

CHANNELS = 1
RATE = 44100
CHUNK = 1024
FORMAT = pyaudio.paInt16

stream = audio.open(
    format=pyaudio.paInt16,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
)

for i in range(100):
    data = stream.read(CHUNK)
    frames.append(data)

wf = wave.open('hoge.wav', 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

stream.stop_stream()
stream.close()
