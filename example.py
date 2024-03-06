import genevative
import numpy as np
def i1(freq, dur, vel, hz):
    env = np.resize(np.linspace(1, 0, int(dur*1/4)), int(dur))
    #bend = np.linspace(0,1,len(arr))**3
    #iar = np.interp(bend, np.linspace(0,1, len(arr)), arr)*0.1
    return np.resize(np.linspace(-1, 1, int(freq)), int(dur))*vel*env
def i2(freq, dur, vel, hz):
    return (np.random.rand(dur)*2 - 1)*np.append(np.linspace(0, 1, int(1/4*dur)), np.zeros(int(3/4*dur)))
def i3(freq, dur, vel, hz):
    env = np.resize(np.linspace(1, 0, int(dur*2/3)), int(dur))
    return np.resize(np.sin(np.sin(np.linspace(-1,1,int(freq))*2*np.pi)*2*np.pi), int(dur))*vel*env
t = genevative.Tracker()
t.add_pattern(
        [[440, 1, 1],
         [i1, 1, 1, 1],
         [i1, 1, 1, 1],
         [i1, 1/3, 2, 1],
         [i1, 1, 1/2, 1],
         [i1, 1, 1, 1],
         [i1, 3/1, 1, 1],
         [i1, 1, 1, 1],
         [i1, 2/3, 1/2, 1],
         [i1, 1, 1/3, 1],
         [i1, 1, 1, 1],
         [i1, 1, 1/2, 1],
         [i1, 1, 1/4, 1],
         [i1, 1, 1, 1],
         [i1, 1, 1, 1],
         [i1, 2, 1/2, 0.75]])
t.add_pattern(
        [[1, 1, 1],
         [i2, 1, 1],
         [i2, 1/2, 1],
         [i2, 2, 1],
         [i2, 1, 1],
         [i2, 1, 1],
         [i2, 3, 1],
         [i2, 7/3, 1],
         [i2, 1, 1],
         [i2, 1/3, 1],
         [i2, 1, 1]])
t.add_pattern(
        [[440, 1, 1],
         [i3, 3/2, 1/3, 0.5],
         [i3, 1, 7/3, 1],
         [i3, 1, 1/3, 1],
         [i3, 1/2, 10/3, 2],
         [i3, 3/2, 2, 1/4],
         [i3, 1, 4/3, 2],
         [i3, 3/2, 1/3, 1],
         [i3, 1/2, 3, 1],
         [i3, 3/2, 1/3, 1]])
t.render()
