import numpy as np
from scipy.io.wavfile import write as wav_render
class Tracker():
    def __init__(self, hz = 44100, v = 1):
        self.sample_rate = hz
        self.volume = v
        self.__raw_instr = []
        self.__raw_pattern = []
    def add_instr(self, instr):
        self.__raw_instr.append(instr)
        return len(self.__raw_instr)
    def add_pattern(self, pattern):
        self.__raw_pattern.append(pattern)
        return len(self.__raw_pattern)
    def render(self):
        freq = 440
        dur = 1
        vel = 1
        pre_rendered = []
        rendered = []
        for pat_num, pattern in enumerate(self.__raw_pattern):
            total_freq = 1
            total_dur = 1
            total_vel = 1
            total_len = 1
            curr_pattern = np.array([], dtype="float64")
            for n, line in enumerate(pattern):
                if n == 0:
                    freq = line[0]
                    dur = line[1]
                    vel = line[2]
                    continue
                line_len = len(line)
                if line_len > 0:
                    instr = line[0]
                else:
                    instr = lambda x,y,w,z:0
                if line_len > 1:
                    freq *= line[1]
                    total_freq *= line[1]
                if line_len > 2:
                    dur *= line[2]
                    total_dur *= line[2]
                if line_len > 3:
                    vel *= line[3]
                    total_vel *= line[3]
                #TODO: make args to fn optional
                curr_pattern = np.append(curr_pattern, instr(self.sample_rate/freq, dur*self.sample_rate, vel, self.sample_rate))
            pre_rendered.append(curr_pattern.copy())
            total_len = len(curr_pattern)/self.sample_rate
            print(f"n:{pat_num:.2f} f:{total_freq:.2f} d:{total_dur:.2f} v:{total_vel:.2f} l:{total_len:.2f}")
            max_len = max([len(i) for i in pre_rendered])
            rendered = np.sum([np.append(i, np.zeros(max_len - len(i))) for i in pre_rendered], axis=0)
            wav_render("out.wav", self.sample_rate, rendered)
