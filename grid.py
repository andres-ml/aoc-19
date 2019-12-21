from space import Point
from collections import defaultdict
from math import inf

class Grid(defaultdict):

    def from_string(self, string):
        self.update({Point((i, j)) : char for j, line in enumerate(string.split('\n')) for i, char in enumerate(list(line))})
        return self

    def bounding_box(self):
        box = [[inf, inf], [-inf, -inf]]
        for point in self:
            box[0][0] = min(box[0][0], point[0])
            box[0][1] = min(box[0][1], point[1])
            box[1][0] = max(box[1][0], point[0])
            box[1][1] = max(box[1][1], point[1])

        return tuple((tuple(box[0]), tuple(box[1])))

    def locate(self, condition):
        return (k for k in self if condition(self[k]))

    def __str__(self, empty=' '):
        box = self.bounding_box()
        char_at = lambda point: self[point] if point in self else empty
        return "\n".join(''.join(char_at(Point((i, j))) for i in range(box[0][0], box[1][0] + 1)) for j in range(box[0][1], box[1][1] + 1))