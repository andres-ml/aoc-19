from utils import cmap, compose, invoker, at, attr
from functools import partial
from itertools import product
from aoc.intcode import Runner

parse = compose(list, cmap(int), invoker('split', ','))

def solve(input, intcode):
    runner = Runner(input)
    runner.run(intcode)
    return intcode, runner

one = compose(at(-1), attr('output'), at(1), partial(solve, [1]), parse)
two = compose(at(-1), attr('output'), at(1), partial(solve, [5]), parse)