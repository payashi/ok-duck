import subprocess
import wave

process = subprocess.Popen(
    ['arecord', '-t', 'wav', '-f', 'S16_LE', '-r', '44100', '-c', '1'],
    stdout=subprocess.PIPE
)

frames = []

try:
    while True:
        data = process.stdout.read(4096)
        frames.append(data)
except KeyboardInterrupt:
    wf = wave.open('record.wav', 'wb')
    wf.setnchannels(1)
    wf.setframerate(44100)
    wf.setsampwidth(2)
    wf.writeframes(b''.join(frames))
    wf.close()

