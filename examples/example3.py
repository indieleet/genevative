import numpy as np
import genevative
import genevative.FX as FX
from os import system
from scipy.signal import fftconvolve
# |%%--%%| <kx03m4KW5W|gYFqzNKQ1Z>


def i1(freq, dur, vel, hz, params):
    return FX.slope(np.resize(np.linspace(-1, 1, int(freq)), int(dur)), dur//2)

def i2(freq, dur, vel, hz, params):
    time = hz//64
    if (time>int(dur)):
        time = int(dur)
    env = np.append(np.ones(time), np.zeros(int(dur-time)))
    return (np.random.rand(int(dur))-0.5)*env
def fx1(arr):
    # mat = (np.resize(FX.slope(np.random.random(44100), int(1/8*44100)),
    #                 int(3*44100)))
    mat = np.sin(np.linspace(0, np.pi, 128))/26
    #mat = np.zeros(65)
    #mat[32] = 1
    c1 = np.convolve(arr[0], mat, mode="same")
    c2 = np.convolve(arr[1], mat, mode="same")
    return np.vstack((c1, c2), dtype=np.float64)

def fx2(arr):
    c1 = FX.delay(arr[0], 44100//2-10, 0.75) + arr[0]
    c2 = FX.delay(arr[1], 44100//2, 0.75) + arr[1]
    return np.vstack((c1, c2), dtype=np.float64)

def fx3(arr):
    c1 = FX.delay(arr[0], 44100//6-10, 0.6) + arr[0]
    c2 = FX.delay(arr[1], 44100//6, 0.61) + arr[1]
    return np.vstack((c1, c2), dtype=np.float64)

def fx4(arr):
    c1 = FX.clip(arr[0], 5)
    c2 = FX.clip(arr[1], 5)
    return np.vstack((c1, c2), dtype=np.float64)
def fx5(arr):
    interp = np.resize(np.sin(np.linspace(0,2*np.pi,44100//3)), arr.shape[-1])*0.00002+np.linspace(0, 1, arr.shape[-1])
    c1 = np.interp(interp, np.linspace(0,1,arr.shape[-1]), arr[0])
    c2 = np.interp(interp, np.linspace(0,1,arr.shape[-1]), arr[1])
    return np.vstack((c1, c2), dtype=np.float64)

silence = lambda f,d,v,h,p:np.zeros(int(d))
# |%%--%%| <gYFqzNKQ1Z|ng31yDiil3>


t = genevative.Tracker()
t.name = "3"
t.volume = 0.25
t.add_pattern(
    [[440, 1, 0.25]] +
    [[i1, 1],
     [],
     [i1, 1/2, 2, 1/2],
     [i1, 3/2, 3/7], [i1, 3/2], [i1, 4/5]]*2 + [[i1, 5/2, 1/3, 1, ("of", 440), ("od", 1), ("rn", 6)], [i1, 3/2, 3/2, 1, ("la", 7/5)],
     [i1, 3/2],
     [i1, 4/5]]*4 +
    [[i1, 2/3, 1, 1,("of", 218), ("rn", 3)],
     [i1, 4/5, 2, 1, ("rn", 2)],
     [silence,1,1/2],
     [i1, 7/3, 1/8, 1/2, ("rn", 6)],
     [i1, 3/2, 1, 1, ("rn", 6)],
     [i1, 4/5, 1, 1, ("rn", 6)],
     [i1, 1, 1, 1, ("of", 329)]
     ])
t.add_pattern([[880,1,1]]+
               [[i1,1,4/3,1, ("of", 880)],
               [],
              [i1,3/2,1]]*6 +
              [[i1, 2/3, 2/3, 1]] +
              [[i1]]*8)
t.add_pattern([[660,1/8,0.2]]+
              [[i2, 9/8],
               [i2, 78/79]]*48 +
              [[i2, 1, 1/3, 1, ("rn", 12)],
               [silence, 1, 64, 1, ("od",4)],
               [i2, 1, 1/4, 1]])
t.render()
t.add_fx(0,fx2)
t.add_fx(2,fx3) 
t.add_fx(0,fx4)
t.add_fx(0,fx1)
t.add_fx(0,fx5)
# t.add_fx(0, lambda arr: FX.clip(arr, 6))
# |%%--%%| <ng31yDiil3|kSQMfPinep>
t.save()
# |%%--%%| <kSQMfPinep|M2bCzvZLBh>
system("ffplay -loop 0 -i 3.wav 2> /dev/null")
