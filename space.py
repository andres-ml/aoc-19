from utils import compose
import operator
import itertools

class Point:

    def __init__(self, *coords):
        self.coords = tuple(coords)
        self.dimension = len(coords)
        pass

    def __eq__(self, point):
        return self.coords == point.coords

    def __lt__(self, point):
        return self.coords < point.coords

    def __add__(self, point):
        return Point(*(a + b for a, b in zip(self.coords, point.coords)))

    def __getitem__(self, index):
        return self.coords[index]

    def __repr__(self):
        return str(self.coords)

    # Access by axis letter. Only supported for 3D or fewer
    def __getattr__(self, letter):
        axisLetters = 'xyz'
        return self.coords[axisLetters.index(letter)]

    def manhattan(self, other):
        return sum(abs(c1 - c2) for c1, c2 in zip(self.coords, other.coords))

    def adjacent(self, distance):
        moves = itertools.product(range(-distance, distance + 1), repeat=self.dimension)
        return (tuple(map(operator.add, self.coords, move)) for move in moves if any(move))