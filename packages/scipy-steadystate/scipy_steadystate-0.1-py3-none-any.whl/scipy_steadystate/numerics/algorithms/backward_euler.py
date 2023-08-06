import numpy as np
from scipy.optimize import root

from scipy_steadystate.numerics import numerical_integration_iterator


def backward_euler(f, x0, dt, t0=0.0, jac=None, return_derivatives=False):
    def y(t, x):
        fjac = None if jac is None else lambda y: dt * jac(t + dt, y) - np.identity(len(y))

        return root(lambda xn: x - xn + dt * f(t + dt, xn), x0=x, jac=fjac).x

    def j(t, x, y):
        return np.identity(len(y)) / (1 - dt * jac(t+dt, y))

    return numerical_integration_iterator(y, x0, dt, t0, jac=j if return_derivatives else None)
