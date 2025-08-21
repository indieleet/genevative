import numpy as np
import genevative
from enum import Enum, auto

class Op(Enum):
    Add = 0
    Sub = auto()
    Mul = auto()
    Div = auto()
    Pow = auto()
    BitAnd = auto()
    BitOr = auto()
    BitXor = auto()
    #BitInv = auto()
    LShift = auto()
    RShift = auto()
    Mod = auto()
    LT = auto()
    LE = auto()
    EQ = auto()
    NE = auto()
    GE = auto()
    GT = auto()
    #Brackets = auto()
    def to_string(self):
        match self:
            case self.Add:
                return "+"
            case self.Sub:
                return "-"
            case self.Mul:
                return "*"
            case self.Div:
                return "//"
            case self.Pow:
                return "**"
            case self.BitAnd:
                return "&"
            case self.BitOr:
                return "|"
            case self.BitXor:
                return "^"
            #case self.BitInv:
            #    return "~"
            case self.LShift:
                return "<<"
            case self.RShift:
                return ">>"
            case self.Mod:
                return "%"
            case self.LT:
                return "<"
            case self.LE:
                return "<="
            case self.EQ:
                return "=="
            case self.NE:
                return "!="
            case self.GE:
                return ">="
            case self.GT:
                return ">"


class Val(Enum):
    Usize = 0
    TVar = auto()
    def to_string(self):
        match self:
            case self.Usize:
                #return repr(np.random.randint(0, np.iinfo(np.uint64).max, None, dtype=np.uint64))
                return repr(np.random.randint(0, 256, None, dtype=np.uint64))
            case self.TVar:
                return "t"

def bbgen(num):
    out = []
    ops = np.random.randint(0, len(Op), num, dtype=np.uint8)
    vals = np.random.randint(0, len(Val), num, dtype=np.uint8)
    #brackets = np.random.randint(0, 2, num, dtype=np.bool)
    out.append(Val(np.random.randint(0, 2, None, dtype=np.bool)).to_string())
    for i in range(num):
        raw_str = " ".join((Op(ops[i]).to_string(), Val(vals[i]).to_string()))
        #if brackets[i]:
        out.insert(0, "(")
        out.append(raw_str)
        out.append(")")
        #else:
        #    out.append(raw_str)
    str_out = " ".join(out)
    if info:
        print(str_out, "\n")
    return str_out

def bb_to_f32(arr: np.array):
    return np.interp(np.linspace(0, 1, int(44100 * len(arr) / 8000)), np.linspace(0, 1, len(arr)), arr.astype(uint8).astype(float32) / 128.0 - 1)

def bbgen_c(num, info=False):
    success = True
    while success:
        out = eval(bbgen(num, info)) 
        if out.any():
            success = False
            out = bb_to_f32(out)
    return out
