def my_zip(*lists):
    res = []
    for i in range(len(lists)):
        res_1 = []
        try:
            for lst in lists:
                res_1.append(lst[i])
        except IndexError:
            break
        res.append(tuple(res_1))
    return res
