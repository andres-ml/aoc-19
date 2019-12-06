from utils import cmap, compose, invoker, at, unpack
from functools import partial
from itertools import product
from aoc.intcode import Runner

N = 100
TARGET = 19690720

parse = compose(list, cmap(int), invoker('split', ','))

runner = Runner()

run = lambda intcode: runner.run(intcode)
alarm = lambda noun, verb: lambda intcode: intcode[:1] + [noun, verb] + intcode[3:]
solve = lambda noun, verb: compose(at(0), run, alarm(noun, verb))
findNounVerb = lambda target, intcode: next((noun, verb) for noun, verb in product(range(N), range(N)) if solve(noun, verb)(intcode) == target)

one = compose(solve(12, 2), parse)
two = compose(unpack(lambda a, b: a * 100 + b), partial(findNounVerb, TARGET), parse)