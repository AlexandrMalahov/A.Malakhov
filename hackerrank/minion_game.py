def minion_game(string):
    # your code goes here
    vowels = 'AEIOU'
    kevin_scores = 0
    stuart_scores = 0
    for i in range(len(string)):
        if s[i] in vowels:
            kevin_scores += len(string) - i
        else:
            stuart_scores += len(string) - i
    if kevin_scores > stuart_scores:
        print('Kevin', kevin_scores)
    elif kevin_scores < stuart_scores:
        print('Stuart', stuart_scores)
    else:
        print('Draw')


if __name__ == '__main__':
    s = 'BANANA'
    minion_game(s)