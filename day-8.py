from utils import cmap, compose, invoker, unpack, chunks
from functools import partial
import re

N = 25
M = 6
L = N * M

BLACK = '0'
WHITE = '1'
TRANSPARENT = '2'

parse = partial(chunks, L)

isOpaque = lambda value: value != TRANSPARENT
showImage = lambda layer: '\n'.join(row for row in (''.join(layer[i:i+N]) for i in range(0, L, N)))

# sub 0s for whitespaces and add a space between columns for readability
makeReadable = compose(partial(re.sub, r'0', ' '), partial(re.sub, r'(0|1)', r'\g<1> '))

one = compose(lambda layer: layer.count('1') * layer.count('2'), partial(min, key=invoker('count', '0')), parse)
two = compose(makeReadable, showImage, list, cmap(compose(next, partial(filter, isOpaque))), unpack(zip), parse)