from functools import reduce, partial
from typing import Callable, Union, Any
import re
import operator

identity = lambda x : x
always = lambda x : lambda *args : x

# function composition. first function may have any arity; the rest must be unary
def compose(*functions) -> Callable:
    ordered = list(reversed(functions))
    return lambda *args: reduce(lambda carry, f: f(carry), ordered[1:], ordered[0](*args))

def cmap(function : Callable) -> Callable:
    return partial(map, function)

def invoker(method : str, *args) -> Callable:
    return lambda object: getattr(object, method)(*args)

def at(index : Union[int, str]) -> Any:
    return lambda indexable: indexable[index]

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
    while not condition(state):
        state = step(state)
    return state

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