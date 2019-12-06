from utils import cmap, compose, invoker, identity
from text import toLines
from functools import partial
from collections import defaultdict

ROOT = 'COM'

parse = compose(list, cmap(invoker('split', ')')), toLines)

def buildOrbits(pairs):
    orbits = defaultdict(list)
    for static, orbiter in pairs:
        orbits[static].append(orbiter)
    return orbits

def countOrbits(source, orbits):
    def count(source, level = 0):
        return level + sum([count(orbiter, level + 1) for orbiter in orbits[source]])
    return count(source)

def path(target, orbits):
    def trace(current):
        orbiters = orbits[current[-1]]
        if len(orbiters) == 0:
            return current if current[-1] == target else None
        paths = (trace(current + [orbiter]) for orbiter in orbiters)
        return next(filter(identity, paths), None)
    return trace([ROOT])

def transfers(origin, destination, orbits):
    originPath = path(origin, orbits)
    destinationPath = path(destination, orbits)
    index = next(i for i, (p1, p2) in enumerate(zip(originPath, destinationPath)) if p1 != p2)
    return len(originPath[index:]) - 1 + len(destinationPath[index:]) - 1

one = compose(partial(countOrbits, ROOT), buildOrbits, parse)
two = compose(partial(transfers, 'YOU', 'SAN'), buildOrbits, parse)