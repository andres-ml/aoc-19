from utils import cmap, compose, invoker, flatten
from functools import partial
from space import Point
from aoc.intcode import Runner
from itertools import count

parse = compose(list, cmap(int), invoker('split', ','))

SCAFFOLD = '#'
VOID = '.'

directions = {
    Point((0, 1)) : 'v',
    Point((-1, 0)) : '<',
    Point((0, -1)) : '^',
    Point((1, 0)) : '>',
}

def draw(intcode):
    runner = Runner()
    runner.run(intcode)
    return runner.output

# drawing (string) to grid (dict)
drawing_to_dict = lambda drawing: {(i, j): char for j, line in enumerate(drawing.split('\n')) for i, char in enumerate(line)}
walkable = lambda coords, grid: coords in grid and grid[coords] != VOID
find_intersections = lambda grid: (coords for coords in grid if walkable(coords, grid) and all(walkable(adjacent, grid) for adjacent in Point(coords).adjacent(1)))
alignment = lambda coords: coords[0] * coords[1]

# I tried to find all paths but it never ends. Instead, I noticed that for both my input and the
# samples, the robot reaches the end by always going in a straight line on intersections. So, we find and use that path:
def find_path(grid):
    robot = next(coords for coords in grid if grid[coords] in '<^>v')
    path = [ Point(robot) ]
    while True:
        adjacent = [p for p in path[-1].adjacent(1) if walkable(p, grid) and (len(path) < 2 or p != path[-2])]
        go_straight = lambda position: -1 if len(path) < 2 or (path[-1] - path[-2]) == (position - path[-1]) else 1
        move = min(adjacent, key=go_straight, default=None)
        # final position reached; exit
        if move is None:
            break
        path.append(move)
    return path

# return R or L depending on whether the current->diretion turn is clockwise(R) or not(L)
def rotation_character(current, direction):
    clockwise_turns = list(directions.values())
    index1 = clockwise_turns.index(current)
    index2 = clockwise_turns.index(direction)
    return 'R' if index1 == (index2 - 1) % len(directions) else 'L'

# path (list of Points) to movements; i.e. pairs of (L|R, move_length)
def path_to_movements(grid, path):
    movement_list = []
    current = next(value for coords, value in grid.items() if value in '<^>v')
    for a, b in zip(path, path[1:]):
        movement = b - a
        direction = directions[movement]
        if current != direction:
            movement_list.append([rotation_character(current, direction), 0])
            current = direction
        movement_list[-1][1] += 1
    return movement_list

# Returns different ways to compress the items by occurrences of consecutive items.
# For example, the list [1,2,3,1,2,3] could be interpreted as:
# ABCABC for A=1 B=2 C=3
# ABAB for A=1,2 B=3
# ABAB for A=1 B=2,3
# AA for A=1,2,3
# This method returns all such encodings.
# The 'max' tells us how many different sequences we can have at most (e.g. max=2 would
# not allow the previous ABCABC sample, since ABC are 3 different sequences)
def compressions(items, max, sequences = []):
    if len(items) == 0:
        return [([], sequences)]
    
    result = []
    for length in range(1, len(items) + 1):
        group = items[0:length]
        # save whether the current sequence was just added or not
        added = False
        if not group in sequences:
            if len(sequences) >= max:
                continue
            sequences.append(group)
            added = True
        for subcompression, subcache in compressions(items[length:], max, sequences[:]):
            result.append(([sequences.index(group)] + subcompression, subcache))
        if added:
            # we don't need this sequence anymore
            sequences = sequences[:-1]
    return result

# compressed movements (main routine + subroutines) to Intcode-ready instructions
def translate_to_instructions(compression):
    names = 'ABC'
    lines = []
    # main routine
    lines.append([names[index] for index in compression[0]])
    # subroutines
    subroutine_to_line = lambda pairs: [str(item) for pair in pairs for item in pair]
    for pairs in compression[1]:
        lines.append(subroutine_to_line(pairs))
    # disable visual feed
    lines.append(['n'])
    return Runner.ASCII_input([','.join(line) for line in lines])

get_grid = compose(drawing_to_dict, partial(''.join), cmap(chr), draw)

# since items are comma-separated, each item will need 2 chars, so compare to 10 not 20
fits_in_memory = lambda l: len(l) <= 10
valid = lambda compression: fits_in_memory(compression[0]) and all(fits_in_memory(flatten(g)) for g in compression[1])
get_instructions = lambda grid: compose(translate_to_instructions, next, partial(filter, valid), partial(compressions, max=3), partial(path_to_movements, grid), find_path)(grid)

def get_dust(intcode):
    grid = get_grid(intcode)
    runner = Runner(get_instructions(grid))
    runner.run([2] + intcode[1:])
    return runner.output[-1]

one = compose(sum, cmap(alignment), find_intersections, get_grid, parse)
two = compose(get_dust, parse)