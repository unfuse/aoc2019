import csv

with open("input5.txt") as csvfile:
    data = list(csv.reader(csvfile))[0]

debugMode = True

def debug(*string):
    if debugMode:
        print(*string)

class InvalidParmMode(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Operation:
    def __init__(self, numParms, opCode, derefsParms):
        self.numParms = numParms
        self.opCode = opCode
        self.derefsParms = derefsParms
        self.instIncr = numParms + 1

    def getParms(self, computer, mods):
        return computer.processParms(mods, self)
    
    def invoke(self, computer, mods):
        pass

class BinaryIntOp(Operation):
    def __init__(self, numParms, opCode, fn):
        super().__init__(numParms, opCode, True)
        self.fn = fn

    def invoke(self, computer, mods):
        parms = [int(x) for x in self.getParms(computer, mods)]
        result = self.fn(parms)
        debug(self.__class__.__name__, "with parms", parms, "and result", result, "stored to", parms[-1])
        computer.write(parms[-1], result)
        computer.moveCur(self.instIncr)
        return True

class InteractiveOp(Operation):
    def __init__(self, numParms, opCode, derefsParms, fn):
        super().__init__(numParms, opCode, derefsParms)
        self.fn = fn

    def invoke(self, computer, mods):
        computer.log()
        parms = self.getParms(computer, mods)
        debug(self.__class__.__name__, "with mode", mods, "and parms", parms)
        self.fn(int(parms[-1]))
        debug("yoohoo")
        computer.moveCur(self.instIncr)
        return True

class InputOp(InteractiveOp):
    def __init__(self):
        super().__init__(1, 3, False, lambda dest: computer.write(dest, int(input("Enter something for the IntCodeComputer: "))))

class OutputOp(InteractiveOp):
    def __init__(self):
        super().__init__(1, 4, True, lambda val: print(val))

class AddOp(BinaryIntOp):
    def __init__(self):
        super().__init__(3, 1, lambda args : args[0] + args[1])

class MulOp(BinaryIntOp):
    def __init__(self):
        super().__init__(3, 2, lambda args : args[0] * args[1])

class TermOp(Operation):
    def __init__(self):
        super().__init__(0, 99, True)
    
    def invoke(self, computer, mod):
        computer.setCur(0)
        return False

class IntCodeComputerProcess():
    def __init__(self):
        
class IntCodeComputer():
    def __init__(self, program, operations):
        self.program = program
        self.operations = operations
        self.cur = 0

    def run(self):
        try:
            while True:
                op, mods = self.processOpCode(self.program[self.cur])
                debug("Mods =", mods)
                debug("OpCode =", op.opCode)
                res = op.invoke(self, mods)
                debug("")
                if res == False:
                    return(self.get())
        except Exception as e:
            print(str(type(e)) + " Error " + str(e))
            return -1

    def processOpCode(self, opCode):
        opIntCode = int(str(opCode)[-2:])
        parmModes = str(opCode)[:-2][::-1]
        op = self.operations[opIntCode]

        if len(parmModes) < op.numParms:
            for i in range(op.numParms - len(parmModes)):
                parmModes += '0'
        elif len(parmModes) == 0 and op.numParms == 0:
            parmModes += '0'

        return (op, parmModes)

    def processParms(self, mods, op):
        numParms = op.numParms
        parmCur = self.cur + 1
        parms = []

        debug("Raw Parms", self.program[self.cur : parmCur + numParms], "with mods", mods)

        for i in range(numParms):
            mod = int(mods[i])
            if mod == 0 or not op.derefsParms: # Address Mode
                parms.append(self.program[int(self.program[parmCur + i])])
            elif mod == 1: # Immediate Mode
                parms.append(self.program[parmCur + i])
            else:
                print("UNKNOWN PARM MODE")
        return parms

    def write(self, idx, mode, val):
        if mode != 0:
            raise InvalidParmMode(mode)

        self.program[idx] = val # only one write mode allowed, address mode

    def read(self, idx, mode):
        if mode == 0: 
            return self.program[int(idx)]
        if mode == 1:
            return int(idx)
        
        raise InvalidParmMode(mode)

    def moveCur(self, val):
        self.cur += val

    def setCur(self, val):
        self.cur = val

    def get(self):
        return read(self.cur, 0)

    def log(self):
        debug("Cur =", self.cur)
        debug("Data =", {i:x for (i,x) in enumerate(self.program)})

operators = [AddOp(), MulOp(), TermOp(), InputOp(), OutputOp()]
operations = {x.opCode:x for x in operators}

# Computer
computer = IntCodeComputer(data, operations)
print(computer.run())


