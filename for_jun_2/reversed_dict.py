def reversed_dict(dictionary):
    new_dict = dict((value, keys) for keys, value in dictionary.items())
    print(new_dict)


reversed_dict({'a': 1, 'b': 1, 'c': 1, 'd': 4})
