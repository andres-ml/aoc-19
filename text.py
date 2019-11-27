import re

# tiny alias for convenience
def toLines(input : str) -> list:
    return input.split('\n')

# returns the values of the groups of the string `line` as matched by `pattern`
# e.g patternGroups(r'I have (\d+) apples and (\d+) pears', 'I have 4 apples and 7 pears') -> ('4', '7')
def patternGroups(pattern : str, line : str) -> tuple:
    return re.match(pattern, line).groups()

# given a dict of patterns, finds the first entry whose key (a pattern) matches `string`, and returns
# the result of applying its transformation over the matching groups from that string
# 
# E.g:
#   switch = patternSwitch({r'([0-9]): int, r'([a-z])': str})
#   patternSwitch('a') -> 'a'
#   patternSwitch('1') -> 1
def patternSwitch(patterns : dict):
    def switch(string : str):
        matching = ((re.match(r'^' + pattern + r'$', string), parser) for pattern, parser in patterns.items())
        return next(parser(*match.groups()) for match, parser in matching if match)
    return switch