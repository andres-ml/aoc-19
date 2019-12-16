from utils import compose, cmap, iterate, skip, at
from functools import partial
from itertools import islice, count, takewhile, accumulate
import operator
import math

PATTERN = [0, 1, 0, -1]

# returns the positions at which the factor at pattern_index appears in the sequence
# that repeats each value in PATTERN repeat_size times
def positions(pattern_index, repeat_size):
    position = pattern_index * repeat_size
    position -= 1 # offset
    for i in count():
        base = len(PATTERN) * repeat_size * i
        yield from range(base + position, base + position + repeat_size)

digitize = lambda n: abs(n) % 10

# we can see the second half of the sequence is just accumulating up the second half of the digits, starting from the end
phase_second_half = compose(list, reversed, list, cmap(digitize), accumulate, reversed)

# calculate phase by doing the regular computation for the first half, and the "optimized" computation for the second
def phase_full(sequence):
    length = len(sequence)
    value_at = lambda index: sum(sequence[j] * factor for factor in [-1, 1] for j in takewhile(lambda j: j < length, positions(PATTERN.index(factor), index + 1)))
    first_half = [digitize(value_at(index)) for index in range(0, length // 2)]
    second_half = phase_second_half(sequence[length // 2:])
    return first_half + second_half

toSequence = compose(list, cmap(int), list, str)
toString = compose(partial(''.join), cmap(str))

find_subsequence = lambda index_slice, repeat_factor: lambda sequence: (sequence * repeat_factor)[(int(toString(sequence[index_slice]))):]

# for part two, we see that the part of the sequence the problem asks us to show belong to the second half of the sequence. since the second half can be
# computed in linear time and does not require knowing the first half, we just trim it at the start and apply phase_second_half instead of phase_full
one = compose(toString, at(slice(0, 8)), next, partial(skip, 100), partial(iterate, phase_full), toSequence)
two = compose(toString, at(slice(0, 8)), next, partial(skip, 100), partial(iterate, phase_second_half), find_subsequence(slice(0, 7), 10000), toSequence)