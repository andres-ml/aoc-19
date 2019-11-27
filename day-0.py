from text import patternGroups, toLines
from utils import compose, cmap, at, dictBuilder
from functools import partial

# Example problem

# Day 0 part 1: input is a list of lines. Each line is an elf holding some cookies.
# We double the amount of cookies for elves appearing in odd positions. What is the final total of cookies?

# Day 0 part 2: We now sort the elves by their name, and then elves in even positions have their cookies multiplied by their position.
# What is the final total of cookies? (Elves in odd positions still have their cookies doubled before sorting)

# Note: positions start from 1

ELF_SPEAK = r'My name is (\w+) and I have (\d+) cookies'

def multiplyCookies(numberedElf, factor, criteria):
    index = numberedElf[0]
    cookies = numberedElf[1]['cookies']
    return (numberedElf[0], {
        'name': numberedElf[1]['name'],
        'cookies': cookies * (factor if criteria(index) else 1)
    })

duplicateCookiesIfOdd = partial(multiplyCookies, factor=2, criteria=lambda index: index % 2 != 0)

one = compose(
    sum,
    cmap(compose(at('cookies'), at(1))),
    cmap(duplicateCookiesIfOdd),
    enumerate,
    cmap(compose(dictBuilder({'name': str, 'cookies': int}), partial(patternGroups, ELF_SPEAK))),
    toLines
)

sortByName = partial(sorted, key=lambda numberedElf: numberedElf[1]['name'])
reenumerate = compose(enumerate, cmap(at(1)))
multiplyCookiesByIndexIfEven = lambda enumeratedElf: multiplyCookies(enumeratedElf, enumeratedElf[0], lambda index: index % 2 == 0)

two = compose(
    sum,
    cmap(compose(at('cookies'), at(1))),
    cmap(multiplyCookiesByIndexIfEven),
    reenumerate,
    sortByName,
    cmap(duplicateCookiesIfOdd),
    enumerate,
    cmap(compose(dictBuilder({'name': str, 'cookies': int}), partial(patternGroups, ELF_SPEAK))),
    toLines
)