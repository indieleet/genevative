import genevative
import numpy as np
from genevative.FX import *
from os import system
# |%%--%%| <kx03m4KW5W|gYFqzNKQ1Z>


def i1(dur, freq, vel, hz):
    return sin(dur, freq)

# |%%--%%| <gYFqzNKQ1Z|ng31yDiil3>


t = genevative.Tracker()
t.name = "3.wav"
t.add_pattern(
    [[440, 1, 1]] +
    [[i1, 1],
     [],
     [i1, 1/2, 2]])
# |%%--%%| <ng31yDiil3|kSQMfPinep>
t.render()
system("ffplay -i 3.wav 2> /dev/null")
