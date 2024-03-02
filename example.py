import genevative
import numpy as np
def i1(freq, dur, vel):
    arr = np.resize(np.linspace(-1,1,freq), freq)*vel
    #bend = np.linspace(0,1,len(arr))**3
    #iar = np.interp(bend, np.linspace(0,1, len(arr)), arr)*0.1
t = genevative.Tracker()
t.add_pattern(
        [[440, 1, 1],
         [i1, 1, 1, 1],
         [i1, 2, 1/2, 0.75]])
#write("test.wav", 44100, iar)
t.render()
