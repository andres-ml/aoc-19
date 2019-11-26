import re

# tiny alias for convenience
def toLines(input : str) -> list:
    return input.split('\n')

# parse a line into a dictionary of properties as defined by `pattern`
# e.g.: toDict(r'I have (\d+) apples and (\d+) pears, {'apples': int, 'pears': int}, 'I have 4 apples and 7 pears') -> {'apples': 4, 'pears': 7}
def toDict(pattern : str, properties : dict, line : str) -> dict:
    regex = re.compile(pattern)
    match = regex.match(line)
    return {key: parser(match.group(index + 1)) for index, (key, parser) in enumerate(properties.items())}

# given a dict of patterns, finds the first entry whose key (a pattern) matches `string`, and returns
# the result of applying its transformation to that string.
# E.g:
#   patternParse({r'[0-9]: int, r'[a-z]': str}, '1') -> 1
#   patternParse({r'[0-9]: int, r'[a-z]': str}, 'a') -> 'a'
def patternParse(patterns : dict, string : str):
    matching = ((re.match(r'^' + pattern + r'$', string), parser) for pattern, parser in patterns.items())
    return next(parser(*match.groups()) for match, parser in matching if match)