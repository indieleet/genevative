import asyncio
import sys

import numpy as np
import sounddevice as sd
from IPython.lib.backgroundjobs import BackgroundJobManager
import time

async def play_buffer(**kwargs):
    loop = asyncio.get_event_loop() 
    event = asyncio.Event()

    def callback(outdata, frame_count, time_info, status):
        global buffer, idx
        if status:
            print(status)
        outdata[:] = buffer[np.arange(idx, idx + frame_count) % len(buffer)]
        idx += frame_count

    stream = sd.OutputStream(callback=callback, dtype=buffer.dtype,
                             channels=buffer.shape[1], **kwargs)
    with stream:
        await event.wait()

def main(): 
    asyncio.run(play_buffer())

def init():
    global buffer, idx
    idx = 0
    buffer = np.reshape(np.sin(np.zeros(1), dtype=np.float32), (-1, 1))
    jobs = BackgroundJobManager()
    jobs.new(main)

def replace(array):
    global buffer, idx
    samplerate = sd.query_devices(0, 'output')['default_samplerate']
    rest = (buffer.shape[0] - idx % buffer.shape[0]) / samplerate
    time.sleep(rest)
    buffer = np.reshape(array.astype(np.float32), (-1, 1))
