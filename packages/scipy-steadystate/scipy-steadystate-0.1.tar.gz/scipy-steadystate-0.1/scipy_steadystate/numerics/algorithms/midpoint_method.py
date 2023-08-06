import numpy as np
from scipy.optimize import root

from scipy_steadystate.numerics import numerical_integration_iterator


def midpoint_method(f, x0, dt, t0=0.0, jac=None, return_derivatives=False):
    def y(t, x):
        fjac = None if jac is None else lambda y: 0.5 * dt * jac(t + 0.5 * dt, 0.5 * (x + y)) - np.identity(len(y))

        return root(lambda xn: x - xn + dt * f(t + 0.5 * dt, 0.5 * (x + xn)), x0=x, jac=fjac).x

    def j(t, x, y):
        p = 0.5 * (x + y)
        tn = t + dt * 0.5
        return (np.identity(len(p)) + 0.5 * dt * jac(tn, p)) / (1 - 0.5 * dt * jac(tn, p))

    return numerical_integration_iterator(y, x0, dt, t0, jac=j if return_derivatives else None)
