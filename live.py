import genevative
import numpy as np
from numpy import *
from genevative import FX as fx
l = genevative.Live()
def linspace(start, stop, num=l.hz, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    return np.linspace(start, stop, num=int(num), endpoint=endpoint, retstep=retstep, dtype=dtype,
             axis=axis, device=device)
replace = l.replace
append = l.append
stop = l.stop
