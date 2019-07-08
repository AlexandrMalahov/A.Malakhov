import textwrap


def merge_the_tools(string, k):
    # your code goes here
    text = textwrap.wrap(string, k)
    lst = []
    for i in range(len(text)):
        lst.append([])
        for j in range(len(text[i])):
            if text[i][j] not in lst[i]:
                lst[i].append(text[i][j])
    for pairs in lst:
        print(''.join(pairs))


if __name__ == '__main__':
    string, k = 'AABCAAADA', 3
    merge_the_tools(string, k)