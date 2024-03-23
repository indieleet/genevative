import genevative
import numpy as np
import genevative.FX as FX
from os import system
# |%%--%%| <kx03m4KW5W|gYFqzNKQ1Z>


def i1(freq, dur, vel, hz, params):
    return FX.slope(FX.sin(int(freq), int(dur)), dur)


def fx1(arr):
    mat = FX.slope(np.resize(np.linspace(-1, 1, 44100//3), 3*44100), 3*44100)
    print(arr)
    c1 = np.convolve(arr[:, 0], mat)
    c2 = np.convolve(arr[:, 1], mat)
    return np.vstack((c1, c2), dtype=np.float64)+arr
# |%%--%%| <gYFqzNKQ1Z|ng31yDiil3>


t = genevative.Tracker()
t.name = "3"
t.add_pattern(
    [[440, 1, 1]] +
    [[i1, 1],
     [],
     [i1, 1/2, 2],
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
system("ffplay -i 3.wav 2> /dev/null")
