from utils import defaultlist
from inspect import getargspec
from collections import defaultdict
from itertools import chain

class Runner:

    N = 100
    HALT = 99

    MODE_POSITIONAL = 0
    MODE_IMMEDIATE = 1
    MODE_RELATIVE = 2

    MEMORY_DEFAULT_VALUE = 0

    opcodeMap = {
        1: 'add',
        2: 'mul',
        3: 'read',
        4: 'show',
        5: 'jit',
        6: 'jif',
        7: 'lt',
        8: 'eq',
        9: 'adjust_relative_base',
    }

    def __init__(self, input = iter([])):
        self.input = input
        methodArity = lambda method: len(getargspec(getattr(self, method))[0]) - 1
        self.instructionArities = {opcode: methodArity(name) for opcode, name in Runner.opcodeMap.items()}
    
    # execute instructions until the program halts
    def run(self, intcode, pointer = 0):
        self.reset(intcode)
        self.intcode = defaultlist(lambda: Runner.MEMORY_DEFAULT_VALUE, intcode)
        while self.intcode[pointer] != Runner.HALT:
            self.intcode, pointer = self.execute(self.intcode, pointer)
        return self.intcode

    # runs code and yields output values until it halts
    def output_iterator(self, intcode, pointer = 0):
        self.reset(intcode)
        while self.intcode[pointer] != Runner.HALT:
            self.intcode, pointer = self.execute(self.intcode, pointer)
            if self.output:
                yield self.output.pop()

    # executes the instruction at pointer
    def execute(self, intcode, pointer):
        opcode, argModes = self.parse_opcode(intcode[pointer])
        instruction, arity = Runner.opcodeMap[opcode], self.instructionArities[opcode]
        pointer += 1
        arguments = intcode[pointer : pointer + arity]
        pointer += arity
        value, movedPointer = getattr(self, instruction)(*[self.mode_value(value, intcode, argModes[i]) for i, value in enumerate(arguments)])
        if value is not None:
            intcode[self.mode_index(intcode[pointer], intcode, argModes[arity])] = value
            pointer += 1
        elif movedPointer is not None:
            pointer = movedPointer
        return intcode, pointer

    def mode_value(self, value, intcode, mode):
        if mode == Runner.MODE_IMMEDIATE:
            return value
        elif mode == Runner.MODE_POSITIONAL:
            return intcode[value]
        elif mode == Runner.MODE_RELATIVE:
            return intcode[value + self.relativeBase]
        raise "Invalid read-from mode"

    def mode_index(self, value, intcode, mode):
        if mode == Runner.MODE_POSITIONAL:
            return value
        elif mode == Runner.MODE_RELATIVE:
            return value + self.relativeBase
        raise "Invalid write-to mode"

    def parse_opcode(self, number):
        argModes = defaultdict(lambda: Runner.MODE_POSITIONAL)
        opcode = number % 100
        number //= 100
        index = 0
        while number > 0:
            argModes[index] = number % 10
            index += 1
            number //= 10
        return opcode, argModes

    def reset(self, intcode):
        self.intcode = defaultlist(lambda: Runner.MEMORY_DEFAULT_VALUE, intcode)
        self.relativeBase = 0
        self.output = []

    # "appends" a value to the current input iterator
    def feed(self, value):
        self.input = chain(self.input, iter([value]))

    #####################################  operations ##########################################
    
    def add(self, x, y):
        return x + y, None

    def mul(self, x, y):
        return x * y, None

    def read(self):
        value = next(self.input)
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

    def adjust_relative_base(self, x):
        self.relativeBase += x
        return None, None