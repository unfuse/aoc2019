debugMode = False

def debug(*string):
    if debugMode:
        print(*string)

class InvalidParmMode(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

READ, WRITE = range(2)
ADDR, IMMD, REL = range(3)
JUMP, NOJUMP = range(2)
CONTINUE, PAUSE, TERMINATE = range(3)

class Operation:
    def __init__(self, opCode, argMetaData):
        self.argMetaData = argMetaData
        self.numParms = len(argMetaData)
        self.opCode = opCode
        self.instIncr =  self.numParms + 1 # + 1 to count for op position in program
    
    def invoke(self, computer, mods):
        return CONTINUE

class BinaryIntOp(Operation):
    def __init__(self, opCode, fn):
        super().__init__(opCode, {0: READ, 1: READ, 2: WRITE})
        self.fn = fn

    def invoke(self, computer, mods):
        parms = computer.processParms(mods, self)
        result = self.fn(parms[0], parms[1])
        debug(self.__class__.__name__, "with parms", parms, "and result", result, "stored to", parms[-1])
        computer.write(parms[2], int(mods[2]), result)
        computer.moveCur(self.instIncr)
        return super().invoke(computer, mods)

class JumpOp(Operation):
    def __init__(self, opCode, fn):
        super().__init__(opCode, {0: READ, 1: READ})
        self.fn = fn

    def invoke(self, computer, mods):
        parms = computer.processParms(mods, self)
        result = self.fn(parms[0])
        debug(self.__class__.__name__, "with parms", parms, "and JUMP", result==JUMP)

        if result == JUMP:
            computer.setCur(parms[1])
        else:
            computer.moveCur(self.instIncr)
        return super().invoke(computer, mods)
        

class InputOp(Operation):
    def __init__(self):
        super().__init__(3, {0: WRITE})

    def invoke(self, computer, mods):
        parms = computer.processParms(mods, self)
        debug(self.__class__.__name__, "with mode", mods, "and parms", parms)
        (value, status) = computer.inputSource.getValue()
        if (status == PAUSE):
            return PAUSE

        computer.write(parms[0], int(mods[0]), value)
        computer.moveCur(self.instIncr)
        return super().invoke(computer, mods)

class OutputOp(Operation):
    def __init__(self):
        super().__init__(4, {0: READ})

    def invoke(self, computer, mods):
        parms = computer.processParms(mods, self)
        debug(self.__class__.__name__, "with mode", mods, "and parms", parms)
        computer.outputSource.putValue(parms[0])
        computer.moveCur(self.instIncr)
        return super().invoke(computer, mods)

class RelOffUpdateOp(Operation):
    def __init__(self):
        super().__init__(9, {0: READ})

    def invoke(self, computer, mods):
        parms = computer.processParms(mods, self)
        debug(self.__class__.__name__, "with mode", mods, "and parms", parms, "and old reloff", computer.relOff)
        computer.relOff += parms[0]
        computer.moveCur(self.instIncr)
        return super().invoke(computer, mods)

class TermOp(Operation):
    def __init__(self):
        super().__init__(99, {})
    
    def invoke(self, computer, mod):
        return TERMINATE

class JumpTrueOp(JumpOp):
    def __init__(self):
        super().__init__(5, lambda a : JUMP if a != 0 else NOJUMP)

class JumpFalseOp(JumpOp):
    def __init__(self):
        super().__init__(6, lambda a : JUMP if a == 0 else NOJUMP)

class AddOp(BinaryIntOp):
    def __init__(self):
        super().__init__(1, lambda a, b : a + b)

class MulOp(BinaryIntOp):
    def __init__(self):
        super().__init__(2, lambda a, b : a * b)

class LessThanOp(BinaryIntOp):
    def __init__(self):
        super().__init__(7, lambda a, b : 1 if a < b else 0)

class EqualsOp(BinaryIntOp):
    def __init__(self):
        super().__init__(8, lambda a, b : 1 if a == b else 0)

class InputSource():
    def __init__(self):
        pass

    def storeValue(self, value):
        pass

    def getValue(self):
        pass

class KeyboardInput(InputSource):
    def __init__(self):
        super().__init__()

    def getValue(self):
        return (int(input("Enter something for the Intcode Computer: ")), CONTINUE)

class StreamInput(InputSource):
    def __init__(self):
        self.values = []
        self.cur = 0

    def storeValue(self, val):
        self.values.append(int(val))

    def getValue(self):
        if (self.cur >= len(self.values)):
            return (0, PAUSE)
        val = self.values[self.cur]
        self.cur += 1
        return (val, CONTINUE)

class ArrayInput(StreamInput):
    def __init__(self, arr):
        super().__init__()
        self.values = arr
        self.cur = 0

    def storeValue(self, val):
        self.arr.append(int(val))

    def getValue(self):
        return super().getValue()

class OutputSource():
    def __init__(self):
        pass

    def putValue(self):
        pass

class PrintOutput(OutputSource):
    def __init__(self):
        super().__init__()

    def putValue(self, val):
        print(val)

class StreamOutput(OutputSource):
    def __init__(self, dest):
        super().__init__()
        self.dest = dest

    def putValue(self, val):
        self.dest.storeValue(val)

class ArrayOutput(OutputSource):
    def __init__(self, arr):
        super().__init__()
        self.arr = arr

    def putValue(self, val):
        self.arr.append(val)

class IntCodeComputer():
    def __init__(self, program, operations, inputSource, outputSource):
        self.program = program
        self.program.extend([0] * 4096)
        self.operations = operations
        self.inputSource = inputSource
        self.outputSource = outputSource
        self.cur = 0
        self.relOff = 0

    def run(self):
        while True:
            op, mods = self.processOpCode(self.program[self.cur])
            debug("Cur =", self.cur)
            debug("OpCode =", op.opCode, "Mods =", mods)
            res = op.invoke(self, mods)
            debug("")
            if res != CONTINUE:
                return res

    def processOpCode(self, opCode):
        opIntCode = int(str(opCode)[-2:])
        parmModes = str(opCode)[:-2][::-1]
        op = self.operations[opIntCode]

        if len(parmModes) < op.numParms:
            for i in range(op.numParms - len(parmModes)):
                parmModes += str(ADDR)
        elif len(parmModes) == 0 and op.numParms == 0:
            parmModes += str(ADDR)

        return (op, parmModes)

    def processParms(self, mods, op):
        debug("Raw Sequence", self.program[self.cur : self.cur + 1 + op.numParms])

        parms = []
        for parmNum, parmType in op.argMetaData.items():
            parmCur = self.cur + 1 + parmNum # skip instr code at self.cur
            if parmType == WRITE:
                parms.append(self.read(parmCur, IMMD))
            elif parmType == READ:
                parms.append(self.read(parmCur, int(mods[parmNum])))
            else:
                print("UNKNOWN PARM MODE")

        return parms

    def write(self, idx, mode, val):
        if int(mode) == ADDR: 
            self.program[int(idx)] = val
        elif int(mode) == REL:
            self.program[self.relOff + int(idx)] = val
        else: 
            raise InvalidParmMode(mode)

    def read(self, idx, mode):
        if int(mode) == ADDR: 
            return int(self.program[int(self.program[int(idx)])])
        if int(mode) == IMMD:
            return int(self.program[int(idx)])
        if int(mode) == REL:
            return int(self.program[self.relOff + int(self.program[int(idx)])])
        
        raise InvalidParmMode(mode)

    def moveCur(self, val):
        self.cur += val

    def setCur(self, val):
        self.cur = val

    def get(self):
        return self.read(self.cur, ADDR)

    def log(self):
        debug("Cur =", self.cur)
        debug("Data =", {i:x for (i,x) in enumerate(self.program)})

operators = [AddOp(), MulOp(), TermOp(), InputOp(), OutputOp(), JumpTrueOp(), JumpFalseOp(), LessThanOp(), EqualsOp(), RelOffUpdateOp()]
operations = {x.opCode:x for x in operators}

def defaultInteractiveComputer(data):
    return IntCodeComputer(data, operations, KeyboardInput(), PrintOutput())

def defaultComputerWithSources(data, inputSource, outputSource):
    return IntCodeComputer(data, operations, inputSource, outputSource)