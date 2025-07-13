import asyncio
import sys

import numpy as np
import sounddevice as sd
from IPython.lib.backgroundjobs import BackgroundJobManager
import time


class Live():

    def __init__(self):
        self.idx = 0
        self.buffer = np.reshape(np.sin(np.zeros(1), dtype=np.float32), (-1, 1))
        self.jobs = BackgroundJobManager()
        self.samplerate = sd.query_devices(0, 'output')['default_samplerate']
        self.jobs.new(self.main)

    async def play_buffer(self, **kwargs):
        loop = asyncio.get_event_loop() 
        event = asyncio.Event()

        def callback(outdata, frame_count, time_info, status):
            if status:
                print(status)
            outdata[:] = self.buffer[np.arange(self.idx, self.idx + frame_count) % len(self.buffer)]
            self.idx += frame_count

        stream = sd.OutputStream(callback=callback, dtype=self.buffer.dtype,
                                 channels=self.buffer.shape[1], **kwargs)
        with stream:
            await event.wait()

    def main(self): 
        asyncio.run(self.play_buffer())


    def replace(self, array, immediate=False):
        if not immediate:
            rest = (self.buffer.shape[0] - self.idx % self.buffer.shape[0]) / self.samplerate
            time.sleep(rest)
        self.buffer = np.reshape(array.astype(np.float32), (-1, 1))
    
    def append(self, array, immediate=False, loop=True, loop_source=True):
        length = max(self.buffer.shape[0], array.shape[0])
        if loop_source:
            self.buffer = np.resize(self.buffer, (length, 1))
        if loop:
            array = np.resize(array, (length, 1))
        if not immediate:
            rest = (self.buffer.shape[0] - self.idx % self.buffer.shape[0]) / self.samplerate
            time.sleep(rest)
        self.buffer[:array.shape[0]] = self.buffer[:array.shape[0]] + array.astype(np.float32)
