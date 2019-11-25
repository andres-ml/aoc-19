from functools import reduce, partial
from typing import Callable, Union, Any
import re

def compose(*functions) -> Callable:
    return lambda x: reduce(lambda carry, f: f(carry), reversed(functions), x)

def cmap(function : Callable) -> Callable:
    return partial(map, function)

def invoker(method : str, *args) -> Callable:
    return lambda object: getattr(object, method)(*args)

def at(index : Union[int, str]) -> Any:
    return lambda indexable: indexable[index]

# build a function that takes some arguments and forwards the call to one of `solvers`, as chosen by
# calling the key function with those same arguments. E.g:
# sum1IfOddElseSum3 = dispatcher(lambda n: 'odd' if isOdd(n) else 'even', {'odd': sum1, 'even': sum3})
def dispatcher(key : Callable, solvers : list) -> Callable:
    return lambda *args, **kargs: solvers[key(*args, **kargs)](*args, **kargs)