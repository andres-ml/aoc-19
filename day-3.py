from utils import cmap, compose, invoker, at, unpack, dictBuilder, switch, identity
from text import patternGroups, toLines
from functools import partial
from itertools import product, permutations
from space import Point
import re

CENTER = Point(0, 0)

# split input into lines, and each line (a wire) into a series of steps: [{'direction': 'U', 'length': 23}, {'direction' ....}]
formatStep = compose(dictBuilder({'direction': str, 'length': int}), partial(patternGroups, r'([URDL])(\d+)'))
formatWire = compose(cmap(formatStep), invoker('split', ','))
parseAll = compose(cmap(formatWire), toLines)

# transforms a wire (a list of steps) into a list of segments
def trace(wire):
    edges = [CENTER]
    for stretch in wire:
        edges.append(travel(stretch, edges[-1]))
    return list(zip(edges[:-1], edges[1:]))

# given a wire stretch (e.g. U41) and a starting Point, returns the destination point
def travel(stretch, origin):
    vector = switch(lambda direction, length: direction, {
        'U': lambda direction, length: Point(0, length),
        'R': lambda direction, length: Point(length, 0),
        'D': lambda direction, length: Point(0, -length),
        'L': lambda direction, length: Point(-length, 0),
    })
    return Point(*origin) + vector(**stretch)

# assumes that wire crossing only happens 1 point at a time (i.e. segments in the same line do not intersect, only perpendicular segments do)
isWithinRange = lambda n, range: range[0] <= n <= range[1] or range[0] >= n >= range[1]
segmentsCross = lambda a, b: isWithinRange(b[0].x, [a[0].x, a[1].x]) and isWithinRange(a[0].y, [b[0].y, b[1].y])
segmentIntersection = lambda s1, s2: next((Point(b[0].x, a[0].y) for a, b in permutations([s1, s2]) if segmentsCross(a, b)), None)

# finds the lines of each wire and checks if any pair of lines from different wires intersect
# returns tuples of the form (segment1, segment2, intersection)
findIntersections = compose(
    partial(filter, unpack(lambda a, b, intersection: intersection is not None)),
    lambda segments: ((a, b, segmentIntersection(a, b)) for a, b in product(segments[0], segments[1])),
)

# hydrates Points with their travel cost
def addCosts(segments):
    current = 0
    for (a, b) in segments:
        a.cost = current
        b.cost = current + a.manhattan(b)
        current = b.cost
    return segments

# find intersections, sort by specified criteria, skip (0, 0) and return the score of the first intersection
solve = lambda criteria: compose(criteria, at(1), partial(sorted, key=criteria), findIntersections)

# criteria for parts one and two
distanceToOrigin = unpack(lambda a, b, intersection: intersection.manhattan(CENTER))
travelCost = unpack(lambda a, b, intersection: a[0].cost + a[0].manhattan(intersection) + b[0].cost + b[0].manhattan(intersection))

one = compose(solve(distanceToOrigin), list, cmap(trace), parseAll)
two = compose(solve(travelCost), list, cmap(addCosts), cmap(trace), parseAll)
