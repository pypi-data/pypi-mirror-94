from itertools import tee, islice


def nth(iterable, n, default=None):
    """
    Returns the nth item or a default value

    See https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    return next(islice(iterable, n, None), default)


def take(n, iterable):
    """
    Return first n items of the iterable as a list

    See https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    return list(islice(iterable, n))


def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...

    See https://docs.python.org/3/library/itertools.html#itertools-recipes
    :param iterable:
    :return:
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
