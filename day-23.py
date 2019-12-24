from utils import cmap, compose, invoker, chunk, unpack
from functools import partial
from space import Point
from aoc.intcode import Runner
from itertools import cycle, chain, repeat

parse = compose(list, cmap(int), invoker('split', ','))

class Buffer:

    def __init__(self, list = [], default = None):
        self.list = list
        self.default = default
        self.idle = False

    def __next__(self):
        if self.list:
            return self.list.pop(0)
        else:
            self.idle = True
            return self.default

def run(size, intcode):
    NAT = None

    nodes = [Runner(Buffer([i], -1)) for i in range(size)]
    network = [node.iterator(intcode) for node in nodes]
    output_buffers = [[] for _ in range(size)]
    
    for index in cycle(range(size)):
        iterator = network[index]
        value = next(iterator)
        if value is not None:
            output_buffers[index].append(value)
            if len(output_buffers[index]) == 3:
                address, X, Y = output_buffers[index]
                output_buffers[index] = []

                if address < size:
                    nodes[address].input.list += [X, Y]
                    nodes[address].input.idle = False
                else:
                    NAT = (X, Y)
                
                yield address, X, Y, False
            
        if all(node.input.idle for node in nodes) and NAT is not None:
            address = 0
            X, Y = NAT
            yield address, X, Y, True
            nodes[address].input.list += [X, Y]
            nodes[address].input.idle = False
                

only_NAT = partial(filter, unpack(lambda address, X, Y, NAT_origin: NAT_origin))
first_repeat_Y = lambda packets: next(p2[2] for p1, p2 in chunk(packets, 2) if p1[2] == p2[2])

one = compose(lambda packets: next(Y for address, X, Y, NAT_origin in packets if address == 255), partial(run, 50), parse)
two = compose(first_repeat_Y, only_NAT, partial(run, 50), parse)