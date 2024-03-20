import numpy as np


def saw(self, freq: float | int, dur):
    return np.resize(np.linspace(-1, 1, int(freq)), dur)


def sin(self, freq: float | int, dur):
    return np.resize(np.sin(np.linspace(-1, 1, int(freq))*2*np.pi), dur)


def tri(self, freq: float | int, dur):
    freq = int(freq)
    h_freq = freq // 2
    return np.resize(
        np.append(
            np.linspace(-1, 1, h_freq),
            np.linspace(1, -1, freq - h_freq + 1)[1:]), dur)


def sqr(self, freq: float | int, dur):
    freq = int(freq)
    arr = np.arange(freq)
    return np.resize(np.where(arr > freq//2, 1, 0), int(dur))


def clip(self, arr: np.array, mult=1):
    return np.clip(arr*mult, -1, 1)


def fix(self, arr, n_size):
    return np.interp(np.arange(n_size), np.arange(len(arr)), arr)
