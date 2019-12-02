from inspect import getargspec

arity = lambda f: len(getargspec(f)[0])

# arity() does not work with some built-in functions: https://docs.python.org/3.7/library/inspect.html#inspect.signature
# Use your own functions or wrap the built-in ones.
instructions = {
    1: lambda x, y: x + y,
    2: lambda x, y: x * y,
}

instructionArities = { k: arity(instructions[k]) for k in instructions }

class Runner:

    N = 100
    HALT = 99

    @staticmethod
    def run(intcode, pointer = 0):
        while intcode[pointer] != Runner.HALT:
            opcode = intcode[pointer]
            instruction, arity = instructions[opcode], instructionArities[opcode]
            slots = 1 + arity + 1   # opcode + number of arguments + destination
            *argumentPointers, destination = intcode[pointer+1 : pointer+slots]
            intcode[destination] = instruction(*[intcode[i] for i in argumentPointers])
            pointer += slots
        return intcode
