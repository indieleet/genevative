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
        freq = 1
        dur = 1
        vel = 1
        rendered = []
        for pattern in self.__raw_pattern:
            curr_pattern = []
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
                    instr = lambda x,y,z:0
                if line_len > 1:
                    freq *= line[1]
                if line_len > 2:
                    dur *= line[2]
                if line_len > 3:
                    vel *= line[3]
                #TODO: make args to fn optional
                np.append(curr_pattern, instr(freq, dur, vel))
            pre_rendered.append(curr_pattern.clone())
            max_len = max([len(i) for i in pre_rendered])
            rendered = np.array([np.append(i, np.zeros(max_len - len(i))) for i in pre_rendered])
