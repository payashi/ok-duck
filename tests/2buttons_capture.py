import wave
import threading
import pyaudio
from gpiozero import Button

BUTTON_A = 4
BUTTON_B = 14

CHANNELS = 1
RATE = 44100
CHUNK = 1024
FORMAT = pyaudio.paInt16

audio = pyaudio.PyAudio()
frames = []
# Button.was_held = False
btn_a = Button(BUTTON_A, pull_up=True)
btn_b = Button(BUTTON_B, pull_up=True)

def save_audio(filename):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setframerate(RATE)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.writeframes(b''.join(frames))
    wf.close()
    
def capture_with(btn):
    while True:
        btn.wait_for_press()
        print("Recording started...")

        global frames
        frames = []

        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        while btn.is_pressed:
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()

        btn.wait_for_release()
        print("Recording stopped.")
    
        save_audio("captured.wav")
        print("Audio was saved")

t = threading.Thread(target=capture_with, args=(btn_b,))
t.start()
        
# Shutdown
# audio.terminate()
