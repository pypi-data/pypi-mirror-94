from itertools import count


def numerical_integration_iterator(f, x0, dt, t0=0.0, jac=None):
    x = x0
    if jac is None:
        for i in count():
            x = f(t0 + dt * i, x)
            yield x
    else:
        for i in count():
            t = t0 + dt * i
            y = f(t, x)
            j = jac(t, x, y)
            x = y
            yield x, j
