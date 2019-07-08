def solve(s):
    s = [x.capitalize() for x in s.split(' ')]
    s = ' '.join(s)
    return s


print(solve('hello  world  d  lol'))
