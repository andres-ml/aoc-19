from utils import cmap, compose, attr, unpack
from text import toLines
from functools import partial
from collections import defaultdict
from itertools import islice, cycle
from math import inf as infinity
from space import Point

class Asteroid:

     def __init__(self, coords):
         self.coords = coords
         self.traces = defaultdict(list)

ASTEROID = '#'

buildAsteroids = lambda grid: [Asteroid((j, i)) for i, row in enumerate(grid) for j, column in enumerate(row) if row[j] == ASTEROID]
parse = compose(buildAsteroids, cmap(list), toLines)

# for each asteroid, trace lines to the rest. Such traces are grouped by line/direction; where the line is defined by its slope (k in y=k*x) and
# direction dictates the direction (<=> the other asteroid is to the right of the one we trace from)
def trace(asteroids):
    for i in range(len(asteroids)):
        asteroid = asteroids[i]
        for j in range(i + 1, len(asteroids)):
            other = asteroids[j]
            x, y = (a - b for a, b in zip(asteroid.coords, other.coords))
            slope = (y / x) if x != 0 else infinity
            positive = other.coords > asteroid.coords
            asteroid.traces[(slope, positive)].append(other)
            other.traces[(slope, not positive)].append(asteroid)

    # sort by distance
    for asteroid in asteroids:
        sortByDistance = compose(Point(*asteroid.coords).manhattan, unpack(Point), attr('coords'))
        for slope in asteroid.traces:
            asteroid.traces[slope] = sorted(asteroid.traces[slope], key=sortByDistance)
        
    return asteroids

def laserize(asteroid):
    # sorter of asteroid tracings depending on the laser movement
    def laserSort(slope, positive):
        prioritize_if = lambda value: 0 if value else 1
        startPointingUp = prioritize_if(slope == infinity and not positive)
        clockwise = (prioritize_if(positive), slope)
        return startPointingUp, clockwise
    
    rotation = cycle(sorted(asteroid.traces.keys(), key=unpack(laserSort)))
    while any(asteroid.traces.values()):
        aligned = asteroid.traces[next(rotation)]
        if aligned:
            yield aligned.pop(0)


# since we already split traces by line and direction, we simply need to count how many different line/directions there are
countAdjacent = compose(len, attr('traces'))
one = compose(countAdjacent, partial(max, key=countAdjacent), trace, parse)

formatResult = lambda asteroid: asteroid.coords[0]*100 + asteroid.coords[1]
two = compose(formatResult, next, lambda laser: islice(laser, 200 - 1, None), laserize, partial(max, key=countAdjacent), trace, parse)