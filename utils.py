from functools import reduce, partial
import re

def compose(*functions):
    return lambda x: reduce(lambda carry, f: f(carry), reversed(functions), x)

def cmap(function):
    return partial(map, function)

def invoker(method, *args):
    return lambda object: getattr(object, method)(*args)

def at(index):
    return lambda list: list[index]

class Text:

    @staticmethod
    def toLines(input):
        return input.split('\n')

    @staticmethod
    def toDict(pattern, keys=None, parsers=None):
        regex = re.compile(pattern)
        if keys is None:
            keys = range(regex.groups)
        if parsers is None:
            parsers = [id for _ in range(regex.groups)]
        def _toDict(line):
            match = regex.match(line)
            return {key: parsers[index](match.group(index + 1)) for index, key in enumerate(keys)}
        return _toDict