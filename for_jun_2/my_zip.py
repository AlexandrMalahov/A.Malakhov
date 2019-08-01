def my_zip(*lists):
    for i in range(min(len(lst) for lst in lists)):
        res = []
        for lst in lists:
            res.append(lst[i])
        yield tuple(res)


print(list(my_zip([1, 2, 3, 4], ('a', 'b', 'c'), (1, 2))))
print(list(zip([1, 2, 3, 4], ('a', 'b', 'c'), (1, 2))))
