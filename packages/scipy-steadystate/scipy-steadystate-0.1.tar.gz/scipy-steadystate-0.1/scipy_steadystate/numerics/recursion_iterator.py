def recursion_iterator(f, x0):
    x = x0
    while True:
        x = f(x)
        yield x
