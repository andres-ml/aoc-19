from functools import reduce, partial
from typing import Callable, Union, Any
import re
import operator
import copy
import itertools

identity = lambda x: x
always = lambda x: lambda *args : x
sign = lambda n: n // max(1, abs(n))

# function composition. first function may have any arity; the rest must be unary
def compose(*functions) -> Callable:
    ordered = list(reversed(functions))
    return lambda *args: reduce(lambda carry, f: f(carry), ordered[1:], ordered[0](*args))

def cmap(function : Callable) -> Callable:
    return partial(map, function)

def invoker(method : str, *args) -> Callable:
    return lambda object: getattr(object, method)(*args)

def at(index : Union[int, str]) -> Callable:
    return lambda indexable: indexable[index]

def attr(attribute : str) -> Callable:
    return lambda object: getattr(object, attribute)

# wraps `function` so that its arguments are transformed before calling it.
# each argument at position `i` will be transformed by `callbacks[i]`, if defined.
def useWith(callbacks : list, function : Callable) -> Callable:
    def wrapped(*args):
        arguments = [callback(arg) for arg, callback in zip(args, callbacks)] + args[len(callbacks):]
        return function(*arguments)
    return wrapped

def paramAt(index : int):
    return lambda *args: args[index]

# switch-case as a function. key provides the use case key, `solvers` the callbacks, indexed by use case.
# E.g:
#   multiplyIfEven = switch(lambda n: n % 2: {0: lambda n: n * 2})
#   map(multiplyIfEven, [1,2,3]) -> [1,4,3]
def switch(key : Callable, solvers : list, default : Callable = None) -> Callable:
    def f(*args, **kargs):
        case = key(*args, **kargs)
        return (solvers[case] if case in solvers else default)(*args, **kargs)
    return f

# applies `step` over `state` as many times as necessary until `condition(state)` yields True
def reduceUntil(condition : Callable, step : Callable, state : Any) -> Any:
    return next(x for x in iterate(step, state) if condition(x))

def iterate(function: Callable, item : Any) -> iter:
    while True:
        yield item
        item = function(item)

# wraps function to be called with unpacked args
def unpack(function):
    return unpackWith(identity, function)

# similar to useWith, except there's only 1 callback that takes the same arguments as the original function
# but returns a single argument to be unpacked and used for the function.
def unpackWith(unpacker : Callable, function : Callable):
    return lambda *args, **kargs: function(*unpacker(*args, **kargs))
    
# parse list of properties into a dictionary of properties as defined by `pattern`
# e.g.:
#   builder = dictBuilder({'apples': int, 'pears': int})
#   builder([1, '2']) -> {'apples': 1, 'pears': 2}  (note that 2 is an integer now)
def dictBuilder(properties : dict) -> dict:
    def builder(indexable):
        return {key: parser(indexable[index]) for index, (key, parser) in enumerate(properties.items())}
    return builder

# partial operator. 'name' should be an operator lib function (add, floordiv, gt, etc)
def operation(name : str, b):
    return lambda a : getattr(operator, name)(a, b)

# wraps an unary function so that it executes with that argument but returns that same argument
# instead of the execution return value. Useful to compose class method invocations.
def within(function):
    def inner(arg):
        function(arg)
        return arg
    return inner

# split list into chunks of size 'size'.
# chunks(3, [1,2,3,4,5,6,7,8,9]) -> [[1,2,3], [4,5,6], [7,8,9]]
def chunks(size : int, items : list) -> list :
    return [items[i:i+size] for i in range(0, len(items), size)]

# function that takes an item and returns a copy of that item with one of its properties altered based on its current value
# altered items must support copying (e.g. in some instances, copying an instance that overrides __getattr__ breaks)
def alter(property : str, function : Callable) -> Callable:
    return lambda original: within(lambda copied: setattr(copied, property, function(getattr(copied, property))))(copy.copy(original))

# returns a generator of isolated items and the rest
# e.g. isolate([1,2,3]) -> (1, (2,3)), (2, (1,3)), (3, (1, 2))
def isolate(items : list) -> iter:
    return ((isolated, (other for other in items if other != isolated)) for isolated in items)

# yields an iterator's value by chunks. E.g:
# chunk(itertools.count(), 3) -> (1,2,3), (4,5,6), (7,8,9), ...
def chunk(iterator : iter, size : int) -> iter:
    return itertools.zip_longest(*([iterator] * size))

# memoization/caching decorator with default cache support
# default cache support means you need to call it as @memoize() and not just @memoize
def memoize(cache={}):
    def inner(function):
        def memoized_function(arg):
            if arg not in cache:
                cache[arg] = function(arg)
            return cache[arg]
        return memoized_function
    return inner

# shorthand for itertools.slice(iterable, n, None)
def skip(n : int, iterable : iter) -> iter:
    return itertools.islice(iterable, n, None)
    
# like defaultdict but with a list. Automatically extends the list length with the specified
# factory() value as many positions as needed when getting or setting positions out of bounds (indices only, not slices)
class defaultlist(list):

    def __init__(self, factory = lambda : None, iterable = []):
        self.factory = factory
        self += list(iterable)

    def __getitem__(self, index):
        self.__fill(index)
        return super().__getitem__(index)

    def __setitem__(self, index, value):
        self.__fill(index)
        return super().__setitem__(index, value)

    def __fill(self, index):
        if isinstance(index, int):
            self += [self.factory()] * max([0, index - len(self) + 1])