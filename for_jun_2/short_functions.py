"""
Python 2.7
Write short functions, which takes one argument - list of numbers, and return:
list of squares of numbers, every second element of list, squares of even elements in odd positions.
"""


def square(list_arg):
    """This function returns list of squares of numbers from input list."""

    list_arg = [x**2 for x in list_arg]
    return list_arg


def every_second_element(list_arg):
    """This function returns every second element from input list."""

    list_arg = [list_arg[i] for i in range(1, len(list_arg), 2)]
    return list_arg


def squares_of_even_elements_in_odd_positions(list_arg):
    """This function returns squares of even elements in odd position."""

    new_list = []
    for i in range(len(list_arg)):
        if i % 2 != 0 and list_arg[i] % 2 == 0:
            new_list.append(list_arg[i] ** 2)
    return new_list


if __name__ == '__main__':
    lst = [2, 1, 3, 4, 6, 6, 7, 9]
    print square(lst)
    print every_second_element(lst)
    print squares_of_even_elements_in_odd_positions(lst)
