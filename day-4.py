from utils import compose, invoker, cmap, unpack
from functools import partial
import re

# use a custom generator to efficiently skip ranges of numbers that contain decreasing sequences
def generator(lower, upper):
    current = lower
    while current <= upper:
        index = next((i for i, n in enumerate(current[:-1]) if current[i] > current[i + 1]), None)
        if index is None:
            yield current
            current = str(int(current) + 1)
        else:
            current = current[:index + 1] + current[index] * len(current[index + 1:])

rulesA = [
    lambda password: re.findall(r'(\d)\1', password),
]

rulesB = [
    lambda password: any(len(match) == 2 for match, char in re.findall(r'((\d)\2+)', password)),
]

validator = lambda rules: lambda password: all(rule(password) for rule in rules)

one = compose(len, list, partial(filter, validator(rulesA)), unpack(generator), invoker('split', '-'))
two = compose(len, list, partial(filter, validator(rulesB)), unpack(generator), invoker('split', '-'))