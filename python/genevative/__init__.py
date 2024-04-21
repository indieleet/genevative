import numpy as np
from scipy.io.wavfile import write as wav_render
from typing import Callable

class Tracker():
    """
    Class to create a Tracker.
    You can specify sample rate, volume or name of output file via parameters (t=genevative.Tracker(hz=44100, v=1, name="out")) or via dot (t.sample_rate = 44100, t.volume = 0.5, t.name = "input").
    Available methods:
    add_instr
    add_pattern
    add_fx
    render
    """
    def __init__(self, hz: int=44100, v: float=1, name: str="out"):
        self.sample_rate = hz
        self.volume = v
        self.name = name
        self.master = []
        self.__raw_instr = []
        self.__raw_pattern = []
        self.__raw_proc = [[],]

    def add_instr(self, instr: Callable) -> int:
        """
        Adds instrument that you can use in patter. If you want it.
        """
        self.__raw_instr.append(instr)
        return len(self.__raw_instr)

    def add_pattern(self, pattern: list) -> int:
        """
        Adds pattern to your tracker.
        Specification of pattern:
        * - means that parameter is optional
        [[initial frequency, initial length, initial velocity],
        [instrument of first note*, frequency of first note*, length of first note*, velocity of first note*, first note effect of first note*, second note effect of first note*, ... last note effect of first note*],
        [instrument of second note*, frequency of second note*, length of second note*, velocity of second note*, first note effect of second note*, second note effect of second note*, ... last note effect of second note*],
        ...
        [instrument of last note*, frequency of last note*, length of last note*, velocity of last note*, first note effect of last note*, second note effect of last note*, ... last note effect of last note*]]
        Available note effects:
        0 or ln: Layer new Notes relative to previous
        1 or la: Layer new note Additive
        2 or cf: use Constant Frequency for one line
        3 or cd: use Constant Duration for one line
        4 or cv: use Constant Velocity for one line
        5 or rn: Repeat Note
        6 or sp: Send Parameters
        7 or of: Override current Frequency with constant value
        8 or od: Override current Duration with constant value
        9 or ov: Override current Velocity with constant value
        """
        self.__raw_pattern.append(pattern)
        self.__raw_proc.append([])
        return len(self.__raw_pattern)

    def add_fx(self, pattern_number: int, fx: Callable, aut: list|None = None):
        if pattern_number == "main":
            pattern_number = 0
        if aut == None:
            aut = np.ones(self.master[pattern_number].shape)
        if type(aut) == float:
            aut = np.full(self.master[pattern_number].shape, aut, dtype=np.float64)
        if pattern_number == 0:
            #self.__raw_proc[0].append((fx, aut))
            self.master[0] = fx(self.master[0])*aut + self.master[0]*(1.-aut)
            return None
        self.master[0] = self.master[0] - self.master[pattern_number]
        self.master[pattern_number] = fx(self.master[pattern_number])*aut+ self.master[pattern_number]*(1.-aut)
        self.master[0] = self.master[0] + self.master[pattern_number]

    def render(self):
        freq = 440
        dur = 1
        vel = 1
        pre_rendered = []
        rendered = []
        dur_hist = []
        for pat_num, pattern in enumerate(self.__raw_pattern):
            total_freq = 1
            total_dur = 1
            total_vel = 1
            total_len = 1
            curr_pattern = np.array([[], []], dtype="float64")
            for n, line in enumerate(pattern):
                freq_and_vel = []
                repeats = 1
                params = tuple()
                dur_hist = 0
                if n == 0:
                    freq = line[0]
                    dur = line[1]
                    vel = line[2]
                    continue
                line_len = len(line)
                if line_len > 0:
                    instr = line[0]
                else:
                    def instr(x, y, w, z, p): return np.zeros(int(y))
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
                            dur_hist = dur
                            dur = line[fxi][1]
                        if (line[fxi][0] == 4) or (line[fxi][0] == "cv"):
                            freq_and_vel = [(freq_and_vel[0][0], line[fxi][1])]
                        if (line[fxi][0] == 5) or (line[fxi][0] == "rn"):
                            repeats = line[fxi][1]
                        if (line[fxi][0] == 6) or (line[fxi][0] == "sp"):
                            params = line[fxi][1:]
                        if (line[fxi][0] == 7) or (line[fxi][0] == "of"):
                            freq = line[fxi][1]
                            freq_and_vel = [(freq, freq_and_vel[0][1])]
                        if (line[fxi][0] == 8) or (line[fxi][0] == "od"):
                            dur = line[fxi][1]
                        if (line[fxi][0] == 9) or (line[fxi][0] == "ov"):
                            vel = line[fxi][1]
                            freq_and_vel = [(freq_and_vel[0][0], vel)]
                # TODO: make args to fn optional
                added_line = np.tile(np.sum([instr(self.sample_rate/i[0], dur*self.sample_rate, i[1], self.sample_rate, params) for i in freq_and_vel], axis=0), repeats)
                if added_line.ndim == 1:
                    added_line = np.resize(
                        added_line, (2, added_line.shape[-1]))
                curr_pattern = np.concatenate(
                    (curr_pattern, added_line), axis=1)
                if dur_hist:
                    dur = dur_hist
            #for pat_fx in self.__raw_proc[pat_num + 1]:
            #    curr_pattern = pat_fx(curr_pattern)
            pre_rendered.append(curr_pattern.copy())
            total_len = curr_pattern.shape[-1]/self.sample_rate
            print(
                f"n:{pat_num:d} f:{total_freq:.2f} d:{total_dur:.2f} v:{total_vel:.2f} l:{total_len:.2f}")
        max_len = max([i.shape[-1] for i in pre_rendered])
        all_tracks = [np.concatenate(
            (i, np.zeros((2, max_len - i.shape[-1]))), axis=1) if (max_len != i.shape[-1]) else i for i in pre_rendered]
        rendered = np.sum(all_tracks, axis=0)
        #for pat_fx in self.__raw_proc[0]:
        #    rendered = pat_fx[0](rendered)*pat_fx[1]+rendered*(1.-pat_fx[1])
        self.master = [rendered, *all_tracks]
        #wav_render(f"{self.name}.wav", self.sample_rate, rendered.T)

    def save(self):
        wav_render(f"{self.name}.wav", self.sample_rate, self.master[0].T)
