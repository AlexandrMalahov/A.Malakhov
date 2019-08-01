import sys


def my_cat(file_names):
    for file in file_names:
        with open(file) as f:
            text = f.readlines()
            print('')
            print('Filename: {}'.format(file))
            print('')
            print(' '.join(text))
    return text


my_cat(sys.argv[1:])
