#!/usr/bin/python3
# Entry point for problem executions.
# Each day is contained in a file day-<day>.py and should define two methods: first and second, which
# should take the input as a parameter and return the solution.
# Example usages:
# ./run.py 0
# ./run.py 0 one
# ./run.py 0 two inputs/custom-input.txt

import sys
import importlib

getArg = lambda index, fallback: sys.argv[index] if len(sys.argv) > index else fallback

day = sys.argv[1]
part = getArg(2, 'one')
input_path = getArg(3, './inputs/day-{day}.txt'.format(day=day))
solver = importlib.import_module('day-{day}'.format(day=day))

with open(input_path) as file:
    result = getattr(solver, part)(file.read())
    print(result)
