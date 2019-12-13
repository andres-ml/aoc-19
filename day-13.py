from utils import cmap, compose, invoker, sign, chunk
from functools import partial
from itertools import takewhile
from collections import defaultdict
from aoc.intcode import Runner
       
EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

parse = compose(list, cmap(int), invoker('split', ','))

def execute(runner, intcode):
    return chunk(runner.output_iterator(intcode), 3)

def build_game(intcode):
    result = defaultdict(lambda : EMPTY)
    for x, y, tile in execute(Runner(), intcode):
        result[(x, y)] = tile
    return result

# generator that constantly keeps the pad under the ball
def dumb_AI(game):
    while True:
        ball = next(p for p in game if game[p] == BALL)
        pad = next(p for p in game if game[p] == PADDLE)
        yield sign(ball[0] - pad[0])

# plays game defined by intcode with the provided AI
def play(AI, game, intcode):
    playthrough = execute(Runner(AI(game)), [2] + intcode[1:])
    for x, y, tile in playthrough:
        if x == -1 and y == 0 and count_blocks(game) == 0:
            return tile
        game[(x, y)] = tile

count_blocks = compose(len, list, partial(filter, lambda tile: tile == BLOCK), invoker('values'))

one = compose(count_blocks, build_game, parse)
two = compose(lambda intcode: play(dumb_AI, build_game(intcode), intcode), parse)