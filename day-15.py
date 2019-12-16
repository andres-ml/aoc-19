from utils import cmap, compose, invoker, unpack, skip, at
from functools import partial
from itertools import takewhile
from collections import defaultdict
from aoc.intcode import Runner
from space import Point
from algorithms import BFS

"""
The code for this day is kind of ugly but I'm too tired
"""
       
WALL = 0
EMPTY = 1
OXYGEN = 2

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

parse = compose(list, cmap(int), invoker('split', ','))

movements = [
    (NORTH, Point((0, 1))),
    (SOUTH, Point((0, -1))),
    (WEST, Point((1, 0))),
    (EAST, Point((-1, 0))),
]
        
# since part 2 requires a full scan we leave it like that, but part 1 could once oxygen is found
def full_scan(intcode):
    grid = dict()
    state = ([Point((0, 0))], EMPTY, intcode)

    def explore(position, intcode):
        for input, vector in ((input, vector) for input, vector in movements if position + vector not in grid):
            runner = Runner()
            runner.feed(input)
            generator = runner.output_iterator(intcode)
            tile = next(generator)
            branch_intcode = runner.intcode
            yield position + vector, tile, branch_intcode

    def expand(state):
        path, tile, intcode = state
        return ((path + [position], tile, branch_intcode) for position, tile, branch_intcode in explore(path[-1], intcode) if tile != WALL)

    oxygen_path = None
    for path, tile, _ in BFS(state, expand):
        grid[path[-1]] = tile
        if tile == OXYGEN:
            oxygen_path = path
    
    return grid, oxygen_path

def calculate_minutes(intcode):
    grid, path = full_scan(intcode)
    oxygen_position = path[-1]
    def explore(position):
        yield from (position + vector for input, vector in movements if position + vector in grid and grid[position + vector] == EMPTY)
    def expand(path):
        grid[path[-1]] = OXYGEN
        return (path + [position] for position in explore(path[-1]))
    
    return max(BFS([oxygen_position], expand), key=len)

path_length = lambda path: len(path) - 1

one = compose(path_length, at(1), full_scan, parse)
two = compose(path_length, calculate_minutes, parse)