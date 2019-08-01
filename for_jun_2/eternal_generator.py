def my_eternal_generator(n):
    while True:
        yield n


a = my_eternal_generator(9)

print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))