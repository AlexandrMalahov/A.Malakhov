import sys


def words_count(filename):
    string_count = {}
    with open(filename, 'r') as f:
        string_input = sorted(f.read().lower().split())
    for word in string_input:
        count = 0
        for string in string_input:
            if word == string:
                count += 1
        string_count[word] = count
    return string_count


def print_words(filename):
    words = sorted(words_count(filename).keys())
    for word in words:
        print word + ' ' + str(words_count(filename)[word])


print_words('small.txt')

# def main():
#     if len(sys.argv) != 3:
#         print 'usage: ./wordcount.py {--count | --topcount} file'
#         sys.exit(1)
#
#     option = sys.argv[1]
#     filename = sys.argv[2]
#     if option == '--count':
#         print_words(filename)
#     elif option == '--topcount':
#         print_top(filename)
#     else:
#         print 'unknown option: ' + option
#         sys.exit(1)
#
# if __name__ == '__main__':
#     main()