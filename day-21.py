from utils import cmap, compose, invoker, flatten
from functools import partial
from space import Point
from aoc.intcode import Runner
from itertools import count

parse = compose(list, cmap(int), invoker('split', ','))

def run(code, intcode):
    runner = Runner(Runner.ASCII_input(code))
    runner.run(intcode)
    return runner.output

def output(line):
    # print result (hull damage) if found, otherwise interpret the full output as a debug message
    return line[-1] if line[-1] > 1000 else ''.join(chr(c) for c in line)

LINES_ONE = [
    'OR D J', # tell the droid to jump if his landing position is not a hole
    'OR A T', 'AND B T', 'AND C T', 'NOT T T', 'AND T J' # tell the droid NOT to jump if ALL the positions prior to landing are ground
    
]

# same as part 1, but check that after a jump we're not stuck
LINES_TWO = LINES_ONE + [
    'NOT J T', 'AND J T', # reset T
    'OR E T', 'OR H T', 'AND T J',  # jump only if after jump we can either go forward (E) or jump (H)
]

one = compose(output, partial(run, LINES_ONE + ['WALK']), parse)
two = compose(output, partial(run, LINES_TWO + ['RUN']), parse)