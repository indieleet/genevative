import numpy as np


def saw(freq: float | int, dur: float | int):
    return np.resize(np.linspace(-1, 1, int(freq)), int(dur))


def sin(freq: float | int, dur: float | int):
    return np.resize(np.sin(np.linspace(-1, 1, int(freq))*2*np.pi), int(dur))


def tri(freq: float | int, dur: float | int):
    freq = int(freq)
    h_freq = freq // 2
    return np.resize(
        np.append(
            np.linspace(-1, 1, h_freq),
            np.linspace(1, -1, freq - h_freq + 1)[1:]), int(dur))


def sqr(freq: float | int, dur: float | int):
    freq = int(freq)
    arr = np.arange(freq)
    return np.resize(np.where(arr > freq//2, 1, 0), int(dur))


def clip(arr: np.array, mult=1):
    return np.clip(arr*mult, -1, 1)


def fix(arr, n_size):
    return np.interp(np.arange(int(n_size)), np.arange(len(arr)), arr)


def conv(arr, mat):
    return np.convolve(arr, mat, mode="same")


def slope(arr, dur):
    dur = int(dur)
    return arr*np.append(np.linspace(1, 0, dur), np.zeros(len(arr)-dur))
