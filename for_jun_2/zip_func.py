def my_zip(*lists):
    return (tuple(map(lambda lst: lst[i], lists)) for i in range(min(map(lambda lst: len(lst), lists))))



print(my_zip([1, 2, 3, 4], ('a', 'b', 'c'), (1, 2)))
a = my_zip([1, 2, 3, 4], ('a', 'b', 'c'), (1, 2))
print(next(a))
print(next(a))

