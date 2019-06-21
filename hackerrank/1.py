if __name__ == '__main__':
    marksheet = [['Rachel', -50], ['Mawer', -50], ['Sheen', -50], ['Shaheen', 51], ['Vasya', 25], ['Stepa', 25]]



    #second_highest = sorted(list(set([marks for name, marks in marksheet])))[1]
    #print('\n'.join([a for a,b in sorted(marksheet) if b == second_highest]))
    second_highest_1 = sorted(list(set([marks for name, marks in marksheet])))[1]
    print('\n'.join([a for a, b in sorted(marksheet) if b == second_highest_1]))