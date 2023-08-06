import numpy as np

from scipy_steadystate.numerics import numerical_integration_iterator


def runge_kutta_method(f, x0, dt, t0=0.0, jac=None, return_derivatives=False):
    def y(t, x):
        k1 = f(t, x)
        k2 = f(t + 0.5 * dt, x + dt * 0.5 * k1)
        k3 = f(t + 0.5 * dt, x + dt * 0.5 * k2)
        k4 = f(t + dt, x + dt * k3)
        return x + 0.16666666666666666 * dt * (k1 + 2 * k2 + 2 * k3 + k4)

    def j(t, x, y):
        k1 = f(t, x)
        k2 = f(t + 0.5 * dt, x + dt * 0.5 * k1)
        k3 = f(t + 0.5 * dt, x + dt * 0.5 * k2)

        dk1 = jac(t, x)
        dk2 = jac(t + 0.5 * dt, x + dt * 0.5 * k1) * (np.identity(len(x)) + 0.5 * dt * dk1)
        dk3 = jac(t + 0.5 * dt, x + dt * 0.5 * k2) * (np.identity(len(x)) + 0.5 * dt * dk2)
        dk4 = jac(t + dt, x + dt * k3) * (np.identity(len(x)) + dt * dk3)

        return np.identity(len(x)) + 0.16666666666666666 * dt * (dk1 + 2 * dk2 + 2 * dk3 + dk4)

    return numerical_integration_iterator(y, x0, dt, t0, jac=j if return_derivatives else None)
