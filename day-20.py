from utils import compose, at
from grid import Grid
from space import Point
from algorithms import BFS
from functools import partial
from collections import defaultdict
import re

# Avoid delving too deep in part two. To avoid hardcoding this value, we could
# attempt to find the path as many times as needed with an increasing max_depth limit until a solution is found
MAX_DEPTH = 30

parse = partial(Grid().from_string)

def set_portals(grid):
    matches = lambda pattern, p: p in grid and re.match(pattern, grid[p])
    portals = defaultdict(list)
    def add_portal(first_letter, second_letter, position):
        name = grid[first_letter] + grid[second_letter]
        portals[name].append(Point(position))
    
    for i, j in grid.locate(lambda char: re.match(r'[A-Z]', char)):
        if matches(r'\.', (i + 1, j)):
            add_portal((i - 1, j), (i, j), (i + 1, j))
        elif matches(r'\.', (i - 1, j)):
            add_portal((i, j), (i + 1, j), (i - 1, j))
        elif matches(r'\.', (i, j + 1)):
            add_portal((i, j - 1), (i, j), (i, j + 1))
        elif matches(r'\.', (i, j - 1)):
            add_portal((i, j), (i, j + 1), (i, j - 1))

    # sort portal definitions so the pairs are always [outer, inner]
    upper_left, lower_right = grid.bounding_box()
    in_outer_ring = lambda point: point[0] in [upper_left[0] + 2, lower_right[0] - 2] or point[1] in [upper_left[1] + 2, lower_right[1] - 2]
    outer_first = lambda point: -1 if in_outer_ring(point) else 1
    grid.portals = {name: sorted(pair, key=outer_first) for name, pair in portals.items()}

    return grid

def find(start, loop, grid):
    visited = dict()
    def step(path):
        visited[path[-1]] = True
        position, depth = path[-1]
        directly_adjacent = [(point, depth) for point in position.adjacent(1) if point in grid and grid[point] == '.']
        outer_portals = [(pair[1], depth - (1 if loop else 0)) for pair in grid.portals.values() if len(pair) == 2 and pair[0] == position]
        inner_portals = [(pair[0], depth + (1 if loop else 0)) for pair in grid.portals.values() if len(pair) == 2 and pair[1] == position]
        return [path + [adjacent] for adjacent in directly_adjacent + outer_portals + inner_portals if adjacent not in visited and 0 <= adjacent[1] <= MAX_DEPTH]

    initial = [(grid.portals[start][0], 0)]
    return BFS(initial, step)

reach = lambda target, bfs: next(path for path in bfs if path[-1] == target)

one = compose(lambda path: len(path) - 1, lambda grid: reach((grid.portals['ZZ'][0], 0), find('AA', False, grid)), set_portals, parse)
two = compose(lambda path: len(path) - 1, lambda grid: reach((grid.portals['ZZ'][0], 0), find('AA', True, grid)), set_portals, parse)