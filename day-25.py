from utils import cmap, compose, invoker
from aoc.intcode import Runner

parse = compose(list, cmap(int), invoker('split', ','))

def run(intcode):
    runner = Runner()
    iterator = runner.output_iterator(intcode)
    output = ''
    for ascii in iterator:
        output += chr(ascii)
        if output[-8:] == 'Command?':
            print(output)
            command = input('Input next command:\n')
            runner.input = iter(Runner.ASCII_input([command + '\n']))
    print(output)

one = compose(run, parse)