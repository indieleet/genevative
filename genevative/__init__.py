import numpy as np
from scipy.io.wavfile import write as wav_render


class Tracker():
    def __init__(self, hz=44100, v=1, name="out"):
        self.sample_rate = hz
        self.volume = v
        self.name = f"{name}.wav"
        self.__raw_instr = []
        self.__raw_pattern = []
        self.__raw_proc = [[],]

    def add_instr(self, instr):
        self.__raw_instr.append(instr)
        return len(self.__raw_instr)

    def add_pattern(self, pattern):
        self.__raw_pattern.append(pattern)
        self.__raw_proc.append([])
        return len(self.__raw_pattern)

    def add_fx(self, pattern_number, fx):
        if pattern_number == "main":
            pattern_number = 0
        self.__raw_proc[pattern_number].append(fx)

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
                freq_and_vel = []
                repeats = 1
                if n == 0:
                    freq = line[0]
                    dur = line[1]
                    vel = line[2]
                    continue
                line_len = len(line)
                if line_len > 0:
                    instr = line[0]
                else:
                    def instr(x, y, w, z): return np.zeros(int(y))
                if line_len > 1:
                    freq *= line[1]
                    total_freq *= line[1]
                if line_len > 2:
                    dur *= line[2]
                    total_dur *= line[2]
                if line_len > 3:
                    vel *= line[3]
                    total_vel *= line[3]
                    appended_vel = vel
                freq_and_vel.append((freq, vel))
                if line_len > 4:
                    for fxi in range(4, line_len):
                        if (line[fxi][0] == 0) or (line[fxi][0] == "ln"):
                            if len(line[fxi]) > 2:
                                appended_vel = line[fxi][2]
                            freq_and_vel.extend(
                                [(l_freq[0]*line[fxi][1], appended_vel) for l_freq in freq_and_vel])
                        if (line[fxi][0] == 1) or (line[fxi][0] == "la"):
                            if len(line[fxi]) > 2:
                                appended_vel = line[fxi][2]
                            freq_and_vel.append(
                                (freq*line[fxi][1], appended_vel))
                        if (line[fxi][0] == 2) or (line[fxi][0] == "cf"):
                            freq_and_vel = [(line[fxi][1], freq_and_vel[0][1])]
                        if (line[fxi][0] == 3) or (line[fxi][0] == "cd"):
                            dur = line[fxi][1]
                        if (line[fxi][0] == 4) or (line[fxi][0] == "cv"):
                            freq_and_vel = [(freq_and_vel[0][0], line[fxi][1])]
                        if (line[fxi][0] == 5) or (line[fxi][0] == "rn"):
                            repeats = line[fxi][1]
                # TODO: make args to fn optional
                added_line = np.tile(np.sum([instr(self.sample_rate/i[0], dur*self.sample_rate,
                                                   i[1], self.sample_rate) for i in freq_and_vel], axis=0), repeats)
                curr_pattern = np.append(curr_pattern, added_line)
            for pat_fx in self.__raw_proc[pat_num + 1]:
                curr_pattern = pat_fx(curr_pattern)
            pre_rendered.append(curr_pattern.copy())
            total_len = len(curr_pattern)/self.sample_rate
            print(
                f"n:{pat_num:.2f} f:{total_freq:.2f} d:{total_dur:.2f} v:{total_vel:.2f} l:{total_len:.2f}")
            max_len = max([len(i) for i in pre_rendered])
            rendered = np.sum([np.append(i, np.zeros(max_len - len(i)))
                              for i in pre_rendered], axis=0)
            for pat_fx in self.__raw_proc[0]:
                rendered = pat_fx(rendered)
            wav_render(self.name, self.sample_rate, rendered)
