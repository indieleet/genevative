import genevative
import numpy as np
import genevative.FX as FX
from os import system
from scipy.signal import fftconvolve
# |%%--%%| <kx03m4KW5W|gYFqzNKQ1Z>


def i1(freq, dur, vel, hz, params):
    return FX.slope(np.resize(np.sin(np.linspace(0, 2*np.pi, int(freq))), int(dur)), dur//2)


def fx1(arr):
    mat = (np.resize(FX.slope(np.random.random(44100), int(1/8*44100)),
                     int(3*44100)))
    c1 = fftconvolve(arr[0], mat, mode="same")
    c2 = fftconvolve(arr[1], mat, mode="same")
    return np.vstack((c1, c2), dtype=np.float64)*0.1+arr*0.3
# |%%--%%| <gYFqzNKQ1Z|ng31yDiil3>


t = genevative.Tracker()
t.name = "3"
t.add_pattern(
    [[440, 1, 0.25]] +
    [[i1, 1],
     [],
     [i1, 1/2, 2, 1/2],
     [i1, 3/2, 3/7],
     [i1, 3/2],
     [i1, 4/5]]*2 +
    [[i1, 5/2, 1/3, 1, ("of", 440), ("od", 1), ("rn", 6)],
     [i1, 3/2, 3/2, 1, ("la", 7/5)],
     [i1, 3/2],
     [i1, 4/5]]*4)
t.add_fx(0, fx1)
# t.add_fx(0, lambda arr: FX.clip(arr, 6))
# |%%--%%| <ng31yDiil3|kSQMfPinep>
t.render()
# |%%--%%| <kSQMfPinep|M2bCzvZLBh>

system("ffplay -i 3.wav 2> /dev/null")
