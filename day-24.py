from utils import compose, iterate, skip
from functools import partial
from grid import Grid
import math

N = 5
BUG = '#'
EMPTY = '.'

parse = partial(Grid().from_string)

bug_dies = lambda adjacent_bug_count: adjacent_bug_count != 1
bug_spawns = lambda adjacent_bug_count: adjacent_bug_count in [1, 2]

def evolve(grid):
    adjacent_bugs = lambda position: sum(1 for p in position.adjacent(1) if p in grid and grid[p] == BUG)
    evolved = Grid()
    for position, char in grid.items():
        if char == BUG and bug_dies(adjacent_bugs(position)):
            char = EMPTY
        elif char == EMPTY and bug_spawns(adjacent_bugs(position)):
            char = BUG
        evolved[position] = char
    return evolved

biodiversity_rating = lambda grid: sum(math.pow(2, j*N + i) for i, j in grid if grid[(i, j)] == BUG)

def first_repeat(grid):
    ratings = [biodiversity_rating(grid)]
    while True:
        grid = evolve(grid)
        rating = biodiversity_rating(grid)
        if rating in ratings:
            return rating
        ratings.append(rating)

def space_neighbours(position, depth, space):
    def extra(position):
        looped = []

        # outer
        i, j = position
        if i == 0:
            looped.append(( (N//2 - 1, N//2), depth - 1 ))
        elif i == N - 1:
            looped.append(( (N//2 + 1, N//2), depth - 1 ))
        if j == 0:
            looped.append(( (N//2, N//2 - 1), depth - 1 ))
        elif j == N - 1:
            looped.append(( (N//2, N//2 + 1), depth - 1 ))
        
        # inner
        if i == N//2 and j == N//2 - 1:
            looped += [((index, 0), depth + 1) for index in range(N)]
        elif i == N//2 and j == N//2 + 1:
            looped += [((index, N - 1), depth + 1) for index in range(N)]
        elif i == N//2 - 1 and j == N//2:
            looped += [((0, index), depth + 1) for index in range(N)]
        elif i == N//2 + 1 and j == N//2:
            looped += [((N - 1, index), depth + 1) for index in range(N)]

        return looped
    return [(p, depth) for p in position.adjacent(1) if p in space[depth] and p != (N // 2, N // 2)] + extra(position)

def evolve_space(space):
    empty_grid = lambda: Grid().from_string('\n'.join(''.join('.' for _ in range(N)) for _ in range(N)))
    min_depth = min(space.keys())
    max_depth = max(space.keys())
    
    if any(char == BUG for char in space[min_depth].values()):
        space[min_depth - 1] = empty_grid()
    
    if any(char == BUG for char in space[max_depth].values()):
        space[max_depth + 1] = empty_grid()
    
    evolved = {depth: empty_grid() for depth in space}
    
    for depth, grid in space.items():
        for position, char in ((position, char) for position, char in grid.items() if position != (N // 2, N // 2)):
            bug_count = sum(1 for p, depth in space_neighbours(position, depth, space) if depth in space and space[depth][p] == BUG)
            if char == BUG and bug_dies(bug_count):
                char = EMPTY
            elif char == EMPTY and bug_spawns(bug_count):
                char = BUG
            evolved[depth][position] = char
    
    return evolved
        

def count_bugs(space):
    return sum(1 for depth, grid in space.items() for position, char in grid.items() if char == BUG)

one = compose(math.floor, first_repeat, parse)
two = compose(count_bugs, next, partial(skip, 200), partial(iterate, evolve_space), lambda grid: {0: grid}, parse)