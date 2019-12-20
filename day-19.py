from utils import cmap, compose, invoker, flatten
from functools import partial
from space import Point
from aoc.intcode import Runner
from itertools import count
from time import sleep

parse = compose(list, cmap(int), invoker('split', ','))

def run(input, intcode):
    runner = Runner(iter(input))
    runner.run(intcode)
    return runner.output[-1]

# segment tuple format: (left, right, depth), where left is inclusive but right is not
def find_square(length, intcode):
    # first point at which the beam is constant (to skip empty lines which mess with our range tracking)
    # such point was found by drawing the beam (I deleted the code for that but it's fairly trivial)
    segments = [(6, 7, 4)]
    while True:
        a, b, depth = segments[-1]
        while run([a, depth + 1], intcode) == 0:
            a += 1
        while run([b + 1, depth + 1], intcode) == 1:
            b += 1
        
        segments.append((a, b + 1, depth + 1))

        if len(segments) == length:
            upper, lower = segments[0], segments[length - 1]
            if upper[1] - lower[0] >= length and lower[0] >= upper[0]:
                return lower[0], upper[2]
            segments.pop(0)

one = compose(sum, lambda intcode: [run([i, j], intcode) for i in range(2) for j in range(2)], parse)
two = compose(lambda p: p[0]*10000 + p[1], partial(find_square, 100), parse)