from utils import cmap, compose, operation, reduceUntil, unpack
from text import toLines
from functools import partial

parse = compose(cmap(int), toLines)

fuel = compose(operation('sub', 2), operation('floordiv', 3))
realFuel = lambda mass: reduceUntil(
    unpack(lambda carry, mass: fuel(mass) <= 0),
    unpack(lambda carry, mass: (carry + fuel(mass), fuel(mass))),
    (0, mass)
)[0]

one = compose(sum, cmap(fuel), parse)
two = compose(sum, cmap(realFuel), parse)