def print_formatted(number):
    # your code goes here
    # for i in range(1, number + 1):
    #     lst = [str(int(i)), oct(i)[2:], hex(i)[2:].upper(), bin(i)[2:]]
    #     print('{}  {}  {}  {:<}'.format(lst[0], lst[1], lst[2], lst[3]))

    width = len("{0:b}".format(number))
    for i in range(1, n + 1):
        print("{0:d} {0:{width}o} {0:{width}X} {0:{width}b}".format(i, width=width))

if __name__ == '__main__':
    n = int(input())
    print_formatted(n)