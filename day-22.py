from utils import cmap, compose
from text import toLines
from functools import partial, reduce

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

# not my solution
def find(times, final_position, deck_size, moves):
    offset = lambda value: (value, 0)
    cut = lambda value: (1, -value)
    reverse = lambda : (-1, -1)
    
    a, b = 1, 0
    for move in moves:
        la, lb = locals()[move['move']](*move['args'])
        a = (la * a) % deck_size
        b = (la * b + lb) % deck_size

    modinv = lambda a, n: pow(a, n - 2, n)

    Ma = pow(a, times, deck_size)
    Mb = (b * (Ma - 1) * modinv(a-1, deck_size)) % deck_size
    return ((final_position - Mb) * modinv(Ma, deck_size)) % deck_size
    
one = compose(partial(shuffle_index, 2019, 10007), parse)
two = compose(partial(find, 101741582076661, 2020, 119315717514047), parse)