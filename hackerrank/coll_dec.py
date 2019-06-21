from collections import deque



if __name__ == '__main__':
    n = int(input())
    d = deque()
    for _ in range(n):
        function, *value = input().split(' ')
        if function == 'append':
            d.append(value)
        elif function == 'appendleft':
            d.appendleft(value)
        elif function == 'pop':
            d.pop()
        elif function == 'popleft':
            d.popleft()
    for x in d:
        print(''.join(x), end=' ')





