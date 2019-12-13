from utils import cmap, compose, invoker, at, attr
from functools import partial, reduce
from itertools import permutations
from aoc.intcode import Runner

parse = compose(list, cmap(int), invoker('split', ','))

def solve(input, intcode):
    runner = Runner(iter(input))
    runner.run(intcode)
    return intcode, runner

one = compose(at(-1), attr('output'), at(1), partial(solve, [1]), parse)
two = compose(attr('output'), at(1), partial(solve, [2]), parse)