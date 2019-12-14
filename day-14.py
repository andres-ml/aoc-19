from utils import compose, cmap, invoker, iterate, at, memoize
from text import toLines, patternGroups
from functools import partial
from collections import defaultdict
import re
import math

# build requirements graph (our formulae)
def parseFormulae(lines):
    formulae = dict()
    for line in lines:
        formula = [(chemical, int(amount)) for amount, chemical in map(lambda compound: compound.split(' '), re.findall(r'\d+ [A-Z]+', line))]
        formulae[formula[-1][0]] = {'total': formula[-1][1], 'requirements': formula[:-1]}
    return formulae

# add depths to graph, where ORE has depth 0, items built with ORE 1, items build with items built with ORE 2, etc.
# used for a topological sort when choosing our next chemical reaction
def setDepths(formulae):
    @memoize({'ORE': 0})
    def depth(chemical):
        return 1 + max(depth(other) for other, amount in formulae[chemical]['requirements'])
    for chemical in formulae:
        formulae[chemical]['depth'] = depth(chemical)
    return formulae

# break down the next most complicated chemical in 'materials' into other chemicals as defined on its formula
def react(formulae, materials, fractionable = False):
    chemical = max((chemical for chemical, amount in materials.items() if chemical != 'ORE' and amount > 0), key=lambda chemical: formulae[chemical]['depth'])
    quantity = materials[chemical]
    total = formulae[chemical]['total']
    for other, amount in formulae[chemical]['requirements']:
        factor = quantity / total if fractionable else math.ceil(quantity / total)
        materials[other] += amount * factor
    materials[chemical] = 0
    return materials

# no more chemical reactions needed if we only have ORE
finished = lambda state: all(amount == 0 or chemical == 'ORE' for chemical, amount in state.items())

# finds needed ORE to get the specified materials with the specified formulae
# fractionable=False -> minimum ORE; fractionable=True -> exact ORE (asymptotically)
calculate_ore = lambda materials, fractionable, formulae: next(materials['ORE'] for materials in iterate(partial(react, formulae, fractionable=fractionable), materials) if finished(materials))

# finds how much FUEL we can get with 'available' amount of ORE, then
# find exact ore/fuel ratio, then check how much we can make with it, then
# check and adjust off-by-1 error
def find_fuel(available, formulae):
    ratio = calculate_ore(defaultdict(int, {'FUEL': 1}), True, formulae)
    fuel = math.floor(available / ratio)
    if calculate_ore(defaultdict(int, {'FUEL': fuel}), False, formulae) > available:
        fuel -= 1
    return fuel

one = compose(partial(calculate_ore, defaultdict(int, {'FUEL': 1}), False), setDepths, parseFormulae, toLines)
two = compose(partial(find_fuel, 1e12), setDepths, parseFormulae, toLines)