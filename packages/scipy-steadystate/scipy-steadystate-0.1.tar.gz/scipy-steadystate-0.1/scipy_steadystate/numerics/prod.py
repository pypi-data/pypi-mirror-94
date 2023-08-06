try:
    # Only supported from Python 3.8 and above.
    # See https://docs.python.org/3.8/library/math.html#math.prod
    from math import prod
except ImportError:
    def prod(*iterables, start=1):
        x = start
        for i in iterables:
            for elem in i:
                x *= elem
        return x
