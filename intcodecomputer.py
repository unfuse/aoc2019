debugMode = False

def debug(*string):
    if debugMode:
        print(*string)

class InvalidParmMode(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

READ, WRITE = range(2)
ADDR, IMMD = range(2)
JUMP, NOJUMP = range(2)

class Operation:
    def __init__(self, opCode, argMetaData):
        self.argMetaData = argMetaData
        self.numParms = len(argMetaData)
        self.opCode = opCode
        self.instIncr =  self.numParms + 1 # + 1 to count for op position in program
    
    def invoke(self, computer, mods):
        pass

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
        return True

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
        return True
        

class InputOp(Operation):
    def __init__(self):
        super().__init__(3, {0: WRITE})

    def invoke(self, computer, mods):
        parms = computer.processParms(mods, self)
        debug(self.__class__.__name__, "with mode", mods, "and parms", parms)
        computer.write(parms[0], int(mods[0]), int(input("Enter something for the Intcode Computer: ")))
        computer.moveCur(self.instIncr)
        return True

class OutputOp(Operation):
    def __init__(self):
        super().__init__(4, {0: READ})

    def invoke(self, computer, mods):
        parms = computer.processParms(mods, self)
        debug(self.__class__.__name__, "with mode", mods, "and parms", parms)
        print(parms[0])
        computer.moveCur(self.instIncr)
        return True

class TermOp(Operation):
    def __init__(self):
        super().__init__(99, {})
    
    def invoke(self, computer, mod):
        computer.setCur(0)
        return False

class JumpTrueOp(JumpOp):
    def __init__(self):
        super().__init__(5, lambda a : JUMP if a != 0 else NOJUMP)

class JumpFalseOp(JumpOp):
    def __init__(self):
        super().__init__(6, lambda a : JUMP if a == 0 else NOJUMP)

class AddOp(BinaryIntOp):
    def __init__(self):
        super().__init__(1,lambda a, b : a + b)

class MulOp(BinaryIntOp):
    def __init__(self):
        super().__init__(2, lambda a, b : a * b)

class LessThanOp(BinaryIntOp):
    def __init__(self):
        super().__init__(7, lambda a, b : 1 if a < b else 0)

class EqualsOp(BinaryIntOp):
    def __init__(self):
        super().__init__(8, lambda a, b : 1 if a == b else 0)

class IntCodeComputer():
    def __init__(self, program, operations):
        self.program = program
        self.operations = operations
        self.cur = 0

    def run(self):
        try:
            while True:
                op, mods = self.processOpCode(self.program[self.cur])
                debug("Cur =", self.cur)
                debug("OpCode =", op.opCode, "Mods =", mods)
                res = op.invoke(self, mods)
                debug("")
                if res == False:
                    return(self.get())
        except Exception as e:
            print(type(e), "Error", e)
            return None

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
        if int(mode) != ADDR:
            raise InvalidParmMode(mode)

        self.program[idx] = val # only one write mode allowed, address mode

    def read(self, idx, mode):
        if int(mode) == ADDR: 
            return int(self.program[int(self.program[int(idx)])])
        if int(mode) == IMMD:
            return int(self.program[int(idx)])
        
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

operators = [AddOp(), MulOp(), TermOp(), InputOp(), OutputOp(), JumpTrueOp(), JumpFalseOp(), LessThanOp(), EqualsOp()]
operations = {x.opCode:x for x in operators}

def defaultComputer(data):
    return IntCodeComputer(data, operations)