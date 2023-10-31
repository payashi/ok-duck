import asyncio
import websockets
import numpy as np
import subprocess
import io
import pygame.mixer

uri = 'ws://192.168.200.46:3000'

async def send_audio(ws):
    process = subprocess.Popen(['arecord', '-t', 'raw', '-f', 'S16_LE', '-r', '44100', '-c', '1'], stdout=subprocess.PIPE)
    while True:
        data = process.stdout.read(4096)
        if not data:
            print('Audio input not found')
            continue
        await ws.send(data)

async def receive_audio(ws):
    while True:
        # Receiving audio data from the server
        data = await ws.recv()

        # Play the audio
        chunk = io.BytesIO(data)
        pygame.mixer.music.load(chunk)
        pygame.mixer.music.play()
        print("Playing the audio received from the server")

async def send_receive_audio():
    async with websockets.connect(uri) as ws:
        # send_task = asyncio.create_task(send_audio(ws))
        # receive_task = asyncio.create_task(receive_audio(ws))

        # await asyncio.gather(send_task, receive_task)
        await asyncio.gather(send_audio(ws), receive_audio(ws))

if __name__ == '__main__':
    pygame.mixer.init()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_receive_audio())


