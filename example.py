import genevative
import numpy as np
def i1(freq, dur, vel):
    return np.resize(np.linspace(-1,1,int(freq)), int(dur))*vel
    #bend = np.linspace(0,1,len(arr))**3
    #iar = np.interp(bend, np.linspace(0,1, len(arr)), arr)*0.1
def i2(freq, dur, vel):
    return (np.random.rand(dur)*2 - 1)*np.append(np.linspace(0,1,int(1/4*dur)), np.zeros(int(3/4*dur)))
t = genevative.Tracker()
t.add_pattern(
        [[440, 1, 1],
         [i1, 1, 1, 1],
         [i1, 1, 1, 1],
         [i1, 1/3, 2, 1],
         [i1, 1, 1, 1],
         [i1, 1, 1, 1],
         [i1, 3/1, 1, 1],
         [i1, 1, 1, 1],
         [i1, 2/3, 1/2, 1],
         [i1, 1, 1, 1],
         [i1, 1, 1, 1],
         [i1, 1, 1/2, 1],
         [i1, 1, 1, 1],
         [i1, 1, 1, 1],
         [i1, 1, 1, 1],
         [i1, 2, 1/2, 0.75]])
t.add_pattern(
        [[1, 1, 1],
         [i2,1, 1],
         [i2,1/2, 1],
         [i2,2, 1],
         [i2,1, 1],
         [i2,1, 1],
         [i2,1/3, 1],
         [i2,1, 1]])
#write("test.wav", 44100, iar)
t.render()
