from utils import compose
import operator
import itertools

class Point(tuple):

    def __init__(self, coords):
        self.dimension = len(coords)

    def __add__(self, other):
        return Point(tuple(a + b for a, b in zip(self, other)))

    # Access by axis letter. Only supported for 3D or fewer
    def __getattr__(self, letter):
        axisLetters = 'xyz'
        if letter not in axisLetters:
            raise AttributeError
        return self[axisLetters.index(letter)]

    def manhattan(self, other):
        return sum(abs(c1 - c2) for c1, c2 in zip(self, other))

    def adjacent(self, distance):
        moves = itertools.product(range(-distance, distance + 1), repeat=self.dimension)
        return (tuple(map(operator.add, self, move)) for move in moves if any(move))