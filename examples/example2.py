import genevative
from os import system
import numpy as np
from scipy.io.wavfile import read as wav_open
from scipy.io.wavfile import write as wav_render

# |%%--%%| <Whu4zpA0rU|qUxTkiTIEw>

file = wav_open("out.wav")
block_len = len(file[1]) // 64
new_arr = np.array([], dtype=np.complex64)
for el in np.array_split(file[1], block_len):
    arr = np.roll(np.fft.fft(el), 1)
    arr = np.blackman(len(arr))*arr
    arr = np.fft.ifft(arr)
    new_arr = np.append(new_arr, arr)

# |%%--%%| <qUxTkiTIEw|sInT1QP5sm>

# i = np.fft.fft(file[1]*0.1)
# i = np.roll(i, 16)
# arr = np.fft.ifft(i/np.abs(i**1/2)+200)

# |%%--%%| <sInT1QP5sm|RBlvtITP3n>

print(new_arr)
wav_render("fft.wav", 44100, new_arr.astype(np.float64))

# |%%--%%| <RBlvtITP3n|6u32UKO7JZ>

system("ffplay -i ~/genevative/fft.wav 2> /dev/null")
