import numpy as np
from scipy_steadystate.numerics import numerical_integration_iterator


def forward_euler(f, x0, dt, t0=0.0, jac=None, return_derivatives=False):
    def y(t, x):
        return x + dt * f(t, x)

    def j(t, x, y):
        return np.identity(len(x)) + dt * jac(t, x)

    return numerical_integration_iterator(y, x0, dt, t0, jac=j if return_derivatives else None)
