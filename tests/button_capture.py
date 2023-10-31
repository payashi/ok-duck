import wave
import threading
import pyaudio
from gpiozero import Button

BUTTON_PIN = 4
CHANNELS = 1
RATE = 44100
CHUNK = 1024
FORMAT = pyaudio.paInt16

audio = pyaudio.PyAudio()
frames = []
button = Button(BUTTON_PIN, pull_up=True)

def capture():
    global frames
    frames = []

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )
    while button.is_pressed:
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    

def save_audio(filename):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setframerate(RATE)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.writeframes(b''.join(frames))
    wf.close()
    


try:
    while True:
        button.wait_for_press()
        print("Recording started...")
        t = threading.Thread(target=capture)
        t.start()

        button.wait_for_release()
        t.join()
        print("Recording stopped.")
    
        save_audio("captured.wav")
        print("Audio was saved")
        
except KeyboardInterrupt:
    audio.terminate()
    print("\nProgram terminated")
