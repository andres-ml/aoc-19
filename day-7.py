from utils import cmap, compose, invoker, unpack, at, reduceUntil
from functools import partial, reduce
from itertools import permutations, chain
from aoc.intcode import Runner

parse = compose(list, cmap(int), invoker('split', ','))

# runs Intcode several times by piping their input/output with [phase[index], previousOutput]
def runSequence(sequence, intcode, endCondition, startSignal = 0):
    runners = [Runner(iter([phase])) for phase in sequence]
    runnerIterators = [runner.output_iterator(intcode) for runner in runners]

    # pipe last signal to current runner's input and add its next output signal to signals
    def step(signals, index):
        runners[index].feed(signals[-1])
        signal = next(runnerIterators[index], None)
        return signals + [signal], (index + 1) % len(runners)

    return reduceUntil(endCondition, unpack(step), ([startSignal], 0))[0]

oneLoop = unpack(lambda outputs, index: index == 0 and len(outputs) > 1)
noMoreValues = unpack(lambda outputs, index: outputs[-1] is None)
# -1 to get last in part A; -2 to get last in part B, since B stops on last = None (no more values)
one = compose(max, cmap(at(-1)), lambda intcode: [runSequence(sequence, intcode, oneLoop) for sequence in permutations(range(0, 5))], parse)
two = compose(max, cmap(at(-2)), lambda intcode: [runSequence(sequence, intcode, noMoreValues) for sequence in permutations(range(5, 10))], parse)