from utils import cmap, compose
from text import toLines
from functools import partial, reduce
import math

def parse_move(line):
    if line == 'deal into new stack':
        return {'move': 'reverse', 'args': []}
    if line[0:3] == 'cut':
        return {'move': 'cut', 'args': [int(line[4:])]}
    if line[0:19] == 'deal with increment':
        return {'move': 'offset', 'args': [int(line[20:])]}

parse = compose(list, cmap(parse_move), toLines)

offset = lambda value, index, deck_size: (index * value) % deck_size
cut = lambda value, index, deck_size: (index - value) % deck_size
reverse = lambda index, deck_size: deck_size - index - 1

# given an index i, 0 <= i < deck_size, returns the position of the index pointing to the same
# card of the deck after it has been shuffled
apply_move = lambda index, deck_size, move, args: globals()[move](*args, index, deck_size)
shuffle_index = lambda index, deck_size, shuffle: reduce(lambda index, move: apply_move(index, deck_size, move['move'], move['args']), shuffle, index)

# reverse_offset = lambda value, *args: offset(-value, *args)
# reverse_cut = lambda value, *args: cut(-value, *args)
# reverse_reverse = reverse
# reverse_shuffle = lambda shuffle: [{**move, 'move': 'reverse_' + move['move']} for move in reversed(shuffle)]
    
one = compose(partial(shuffle_index, 2019, 10007), parse)