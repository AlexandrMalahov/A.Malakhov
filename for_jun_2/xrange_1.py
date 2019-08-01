def my_range(*args):
    if len(args) == 1:
        start, stop, step = 0, args[0], 1
    elif len(args) == 2:
        start, stop, step = args[0], args[1], 1
    elif len(args) == 3:
        start, stop, step = args[0], args[1], args[2]

    if len(args) > 3:
        raise TypeError('my_range expected at most 3 arguments, got {}'.format(len(args)))
    elif len(args) == 0:
        raise TypeError('my_range expected at least 1 arguments, got 0')

    if step == 0:
        raise ValueError('my_range() arg 3 must not be zero')


    if start < stop:
        while start < stop:
            yield start
            start += step
    elif start > stop and step < 0:
        while stop < start:
            yield start
            start += step


for i in my_range(1, 10, 1):
    print(i)

int('vgkj5')