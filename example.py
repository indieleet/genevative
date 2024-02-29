import genevative
import numpy as np
from scipy.fft import rfft, irfft, fftshift
from scipy.io.wavfile import write
def i1(freq, dur, vel):
    arr = np.resize(np.linspace(-1,1,44100//440), 2*44100)
    bend = np.linspace(0,1,len(arr))**3
    iar = np.interp(bend, np.linspace(0,1, len(arr)), arr)*0.1
t = genevative.Tracker()
t.add_pattern(
        [[440, 1, 1],
         [i1, 1, 1, 1]]
write("test.wav", 44100, iar)
print(iar)
