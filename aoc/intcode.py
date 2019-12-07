from inspect import getargspec
from collections import defaultdict

class Runner:

    N = 100
    HALT = 99

    MODE_POSITIONAL = 0
    MODE_IMMEDIATE = 1

    opcodeMap = {
        1: 'add',
        2: 'mul',
        3: 'read',
        4: 'show',
        5: 'jit',
        6: 'jif',
        7: 'lt',
        8: 'eq',
    }

    def __init__(self, input = []):
        self.input = input
        methodArity = lambda method: len(getargspec(getattr(self, method))[0]) - 1
        self.instructionArities = {opcode: methodArity(name) for opcode, name in Runner.opcodeMap.items()}
    
    # execute instructions until the program halts
    def run(self, intcode, pointer = 0):
        self.reset()
        while intcode[pointer] != Runner.HALT:
            intcode, pointer = self.execute(intcode, pointer)
        return intcode


    # runs code and yields output values until it halts
    def output_iterator(self, intcode, pointer = 0):
        self.reset()
        while intcode[pointer] != Runner.HALT:
            intcode, pointer = self.execute(intcode, pointer)
            if self.output:
                yield self.output.pop()

    # executes the instruction at pointer
    def execute(self, intcode, pointer):
        opcode, argModes = self.parseOpcode(intcode[pointer])
        instruction, arity = Runner.opcodeMap[opcode], self.instructionArities[opcode]
        pointer += 1
        arguments = intcode[pointer : pointer + arity]
        pointer += arity
        value, movedPointer = getattr(self, instruction)(*[value if argModes[i] == Runner.MODE_IMMEDIATE else intcode[value] for i, value in enumerate(arguments)])
        if value is not None:
            intcode[intcode[pointer]] = value
            pointer += 1
        elif movedPointer is not None:
            pointer = movedPointer
        return intcode, pointer

    def parseOpcode(self, number):
        argModes = defaultdict(lambda: Runner.MODE_POSITIONAL)
        opcode = number % 100
        number //= 100
        index = 0
        while number > 0:
            argModes[index] = number % 10
            index += 1
            number //= 10
        return opcode, argModes

    def reset(self):
        self.inputCursor = 0
        self.output = []

    #####################################  operations ##########################################
    
    def add(self, x, y):
        return x + y, None

    def mul(self, x, y):
        return x * y, None

    def read(self):
        value = self.input[self.inputCursor]
        self.inputCursor += 1
        return value, None

    def show(self, x):
        self.output.append(x)
        return None, None

    def jit(self, x, y):
        return None, y if x != 0 else None

    def jif(self, x, y):
        return None, y if x == 0 else None

    def lt(self, x, y):
        return int(x < y), None

    def eq(self, x, y):
        return int(x == y), None