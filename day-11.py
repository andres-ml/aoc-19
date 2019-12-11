from utils import cmap, compose, invoker, at, attr, unpack
from functools import partial
from itertools import zip_longest
from collections import defaultdict
from space import Point
from aoc.intcode import Runner

BLACK = '.'
WHITE = '#'

class Robot:

    ColorMap = {
        0: BLACK,
        1: WHITE
    }

    LEFT = 0
    RIGHT = 1

    def __init__(self, cpu):
        self.cpu = cpu
        self.position = Point(0, 0)
        self.velocity = Point(0, 1)
        self.painted = dict()

    def paint_all(self, intcode, grid):
        self.cpu.input += [self.read(grid)]
        generator = self.cpu.output_iterator(intcode)
        paired_outputs = zip_longest(*[generator] * 2)
        for color, turn in paired_outputs:
            self.paint_current(grid, color)
            self.velocity.coords = self.turn(turn)
            self.position += self.velocity
            self.cpu.input += [self.read(grid)]

    def read(self, grid):
        return next(k for k, color in Robot.ColorMap.items() if grid[self.position.coords] == color)
    
    def paint_current(self, grid, color):
        grid[self.position.coords] = Robot.ColorMap[color]
        self.painted[self.position.coords] = True

    def turn(self, turn):
        a, b = self.velocity.coords
        if turn == Robot.LEFT:
            return (-b, a)
        elif turn == Robot.RIGHT:
            return (b, -a)
        raise "Invalid turn"
        

parse = compose(list, cmap(int), invoker('split', ','))

def solve(intcode, grid):
    robot = Robot(Runner())
    robot.paint_all(intcode, grid)
    return grid, robot

makeGrid = lambda defaults = {} : defaultdict(lambda: BLACK, defaults)

def display(grid):
    xs = sorted([p[0] for p, color in grid.items() if color == WHITE])
    ys = sorted([p[1] for p, color in grid.items() if color == WHITE])
    paintWhite = lambda color: color if color == WHITE else ' '
    # for some reason we need to flip it vertically for it to display properly
    return '\n'.join(''.join(paintWhite(grid[(i, j)]) for i in range(xs[0], xs[-1] + 1)) for j in range(ys[-1], ys[0] - 1, -1))

one = compose(len, attr('painted'), at(1), unpack(solve), lambda intcode: (intcode, makeGrid()), parse)
two = compose(display, at(0), unpack(solve), lambda intcode: (intcode, makeGrid({(0, 0): WHITE})), parse)