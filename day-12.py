from utils import compose, cmap, attr, alter, isolate, iterate
from text import toLines
from space import Point
from functools import partial, reduce
from itertools import islice
import re
import math

class Body:

    def __init__(self, coords):
        self.position = Point(tuple(coords))
        self.velocity = Point(tuple([0] * self.position.dimension))

parseBody = compose(Body, cmap(int), partial(re.findall, r'-?\d+'))
parse = compose(list, cmap(parseBody), toLines)

sign = lambda n: n // max(1, abs(n))
gravitate = lambda body, towards, velocity: velocity + Point(tuple(sign(b - a) for a, b in zip(body.position, towards.position)))

adjust = lambda system: [alter('velocity', compose(*[partial(gravitate, body, other) for other in rest]))(body) for body, rest in isolate(system)]
move = lambda system: [alter('position', lambda position: position + body.velocity)(body) for body in system]
step = compose(move, adjust)

energy = compose(sum, cmap(abs))
potential = compose(energy, attr('position'))
kinetic = compose(energy, attr('velocity'))
total_energy = lambda system: sum(potential(body) * kinetic(body) for body in system)

# We can see that gravity forces among planets affects each axis independently; i.e. the update to each
# coordinate of the velocity vectors solely depend on the relative positions of the planets along that axis.
# This means repeating cycles happen independently across all axis, so we can find the full-system repeating cycle length
# by computing the least common multiple of all axis cycle lengths.
def first_repeat(system):
    dimension = system[0].position.dimension
    # serializer of one axis for comparison between system states
    serialize_axis = lambda system, axis: [body.position[axis] for body in system] + [body.velocity[axis] for body in system]
    # we assume the initial state belongs to the repeating cycle and is thus the first state to be eventually repeated
    initial = tuple(serialize_axis(system, axis) for axis in range(dimension))
    # store the cycle length for each axis
    cycle_lengths = [0] * dimension
    counted_moving_system = enumerate(iterate(step, system))
    while not all(cycle_lengths):
        count, current = next(counted_moving_system)
        for axis in range(dimension):
            if cycle_lengths[axis] == 0 and serialize_axis(current, axis) == initial[axis]:
                cycle_lengths[axis] = count
    
    least_common_multiple = lambda a, b: a * b // math.gcd(a, b)
    return reduce(least_common_multiple, cycle_lengths)

one = compose(total_energy, next, lambda movingSystem: islice(movingSystem, 1000, None), partial(iterate, step), parse)
two = compose(first_repeat, parse)