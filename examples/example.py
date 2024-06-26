import genevative
import numpy as np
from os import system


def i1(freq, dur, vel, hz, params):
    env = np.resize(np.linspace(0, 1, int(dur)), int(dur)) ** 3
    # bend = np.linspace(0,1,len(arr))**3
    # iar = np.interp(bend, np.linspace(0,1, len(arr)), arr)*0.1
    return np.resize(np.linspace(-1, 1, int(freq)), int(dur)) * vel * env


def i2(freq, dur, vel, hz, params):
    dur1 = 1 / 8
    return (np.random.rand(int(dur)) * 2 - 1) * np.resize(
        np.append(
            np.linspace(0, 1, int(1 / 8 * dur)) ** (11 /
                                                    3), np.zeros(int(7 / 8 * dur))
        ),
        int(dur),
    )


def i3(freq, dur, vel, hz, params):
    env = np.resize(np.linspace(0, 1, int(dur * 1 / 8)), int(dur)) ** 4
    return (
        np.resize(
            np.sin(np.sin(np.linspace(-1, 1, int(freq)) * 2 * np.pi) * 2 * np.pi),
            int(dur),
        )
        * vel
        * env
    )


def i4(freq, dur, vel, hz, params):
    env = np.append(np.linspace(0, 1, hz // 8) ** 4, np.zeros(int(hz * 3 / 8)))
    arr = np.resize(
        np.append(np.sin(np.linspace(-1, 1, int(freq))),
                  np.zeros(int(freq * 3 / 8))),
        int(dur),
    ) * np.resize(env, int(dur))
    bend = np.resize(
        np.append(
            np.linspace(0, 1, len(arr) //
                        8) ** 5, np.zeros(int(len(arr) / 3 * 8))
        ),
        int(dur),
    )
    iar = np.interp(bend, np.linspace(0, 1, len(arr)), arr)
    return iar


t = genevative.Tracker()
t.add_pattern(
    [[440, 4, 1]]
    + [[lambda x, y, w, z, h: np.zeros(int(y)), 1, 1], [i1, 1, 2, 1]]
    + [
        [i1, 1, 1 / 2, 0.25, (0, 3 / 2), (0, 64 / 63), (0, 63 / 64)],
        [i1, 1, 1 / 3, 1, ("cd", 2), ("cf", 100), ("cv", 0.5)],
        [i1, 3 / 1, 1, 0.2, (0, 2), (0, 3), (0, 1 / 2)],
        [i1, 1, 5 / 2, 1 / 0.2],
        [i1, 2 / 3, 3 / 2, 1],
    ]
    * 3
    + [
        [i1, 1, 1 / 2, 0.2, (0, 2), (0, 1 / 6), (0, 1 / 2)],
        [i1, 1, 3 / 2, 1],
        [i1, 2, 1 / 2, 0.75],
    ]
)
t.add_pattern(
    [
        [1, 1, 1],
        [i2, 1, 1 / 2, 1, ("cd", 1/2)],
        [i2, 1, 2, 1],
        [i2, 1, 1 / 6, 1],
        [i2, 1, 1, 1],
        [i2, 1, 1, 1],
        [i2, 1, 1, 1],
        [i2, 1, 1, 1],
        [i2, 1, 1, 1],
        [i2, 1, 8, 1],
        [i2, 1, 7 / 3, 1],
        [i2, 1, 1, 1],
        [i2, 1, 1 / 3, 1],
        [i2, 1, 1, 1],
    ]
)
t.add_pattern(
    [[440, 1, 1]]
    + (
        [
            [i3, 3 / 2, 1 / 3, 0.5, (2, 330)],
            [i3, 1, 7 / 3, 1, (4, 0.1)],
            [i3, 1, 1 / 3, 1],
            [i3, 1 / 2, 10 / 3, 2],
            [i3, 3 / 2, 2, 1 / 4],
            [i3, 1, 4 / 3, 2],
            [i3, 3 / 2, 1 / 3, 1],
            [i3, 1 / 2, 3, 1],
            [i3, 3 / 2, 1 / 3, 1],
        ]
        * 5
    )
)
blops = [[440, 1, 1], [i4], [i4], [i4], [i4], [i4], [i4], [i4], [i4]]
blops.extend(blops[1:] * 5)
t.add_pattern(blops)
t.render()
system("ffplay -i out.wav 2> /dev/null")
