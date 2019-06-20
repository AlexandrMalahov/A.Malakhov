# Доделать!!! Не правильный вывод данных
# https://www.hackerrank.com/challenges/
# merge-the-tools/
# problem?h_r%5B%5D=next-challenge&h_r%5B%5D=next-challenge&h_v
# %5B%5D=zen&h_v%5B%5D=zen&isFullScreen=true&h_
# r=next-challenge&h_v=zen&h_r=next-challenge&h_v=zen&h_r=next-
# challenge&h_v=zen&h_r=next-challenge&h_v=zen&h_
# r=next-challenge&h_v=zen&h_r=next-challenge&h_v=zen&h_r=next-challenge&h_v=zen
import textwrap

def merge_the_tools(string, k):
    # your code goes here
    text = textwrap.wrap(string, k)
    text = list(map(set, text))
    lst = []
    for item in text:
        lst.append(list(item))
    print(lst)
    for item in lst:
        print(''.join(item))


if __name__ == '__main__':
    string, k = 'AABCAAADA', 3
    merge_the_tools(string, k)