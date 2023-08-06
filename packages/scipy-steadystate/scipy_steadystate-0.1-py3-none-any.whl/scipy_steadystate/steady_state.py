import numpy as np
from scipy.optimize import root

from scipy_steadystate.itertools import take, nth
from scipy_steadystate.numerics import prod, numerical_integration_iterator
from scipy_steadystate.numerics.algorithms import (
    backward_euler, forward_euler, midpoint_method, trapezoidal_rule, runge_kutta_method
)


def steady_state(sf,
                 T,
                 x0,
                 t0=0.0,
                 steps=10,
                 jac=None,
                 integration_method='forward-euler'):
    """
    Finds the periodic steady state solution of a given state equation system.

    A periodic steady state is found when the state a t=t0 is equal to the one after the
    periodic time t+T, i.e. sf(t0) = sf(t0 + T). This method explicitly is for non LTI-systems,
    however the system must be assembled out of periodic systems

    Periodic steady states usually happen only if all elements comprising the system are
    themselves periodic. If more than one periodic state source exists, the overall periodic time
    T will become the least common multiple (LCM) extended for decimals.
    E.g.
    - for one periodic source having an intrinsic time of T1 = 2s, T = T1 = 2s.
    - for two periodic sources: T1 = 2s, T2 = 3s, T = LCM(T1, T2) = 6s
    - and so on.

    :param sf:
        The state equations. Must be a function with two input parameters; time `t` and state `x`.
    :param T:
        The intrinsic period time T known ahead of computing steady state.
    :param t0:
        The start time t0. For proper systems setting this value should be unnecessary.
    :param x0:
        Initial guess for the steady state solution.
    :param steps:
        The number of computation steps to perform for numerical integration of the steady equations.
        The more steps performed, the more accurate the result with less artifacts but the slower the computation.
    :param jac:
        Jacobian of the state function `sf`. Takes two arguments `t` and `x`.
    :param integration_method:
        The integration method to perform. Supported values are:
        - `euler`/`forward-euler`: Performs the most simple form of integration: x2 = x1 + dt * sf(t, x1)
        - `runge-kutta-method`/`runge-kutta`/`rk4`: "The" explicit Runge-Kutta-Method (alias RK4).
        - `backward-euler`: Simplest implicit integration method: x2 = x1 + dt * sf(t+dt, x2)
        - `trapezoidal`/`trapezoidal-rule`: Trapezoidal rule which averages the value between the current and next step:
          x2 = x1 + dt / 2 * (sf(t, x1) + sf(t+dt, x2))
        - `midpoint`/`midpoint-method`: Midpoint method that uses the value between the current and next step:
          x2 = x1 + dt * sf(t+dt/2, (x1+x2)/2)
        - `custom`: Support for custom numerical integrators. This is especially useful if you have specific needs,
          such as not yet implemented algorithms, performance improvements (e.g. different solvers for implicit methods)
          or explicit next-step solutions for implicit methods for certain simple functions.
          With `custom`, Jacobians (`jac`) must take an additional argument `y` that will hold the next computed value
          from `sf`. Implicit methods rely on `y` to exactly obtain derivatives.
    :return:
    """
    dt = T / steps

    if integration_method == 'forward-euler' or integration_method == 'euler':
        def create_integration_series(x0):
            return forward_euler(sf, x0, dt, t0, jac, return_derivatives=jac is not None)

    elif integration_method == 'runge-kutta-method' or integration_method == 'runge-kutta' or integration_method == 'rk4':
        def create_integration_series(x0):
            return runge_kutta_method(sf, x0, dt, t0, jac, return_derivatives=jac is not None)

    elif integration_method == 'backward-euler':
        def create_integration_series(x0):
            return backward_euler(sf, x0, dt, t0, jac, return_derivatives=jac is not None)

    elif integration_method == 'trapezoidal' or integration_method == 'trapezoidal-rule':
        def create_integration_series(x0):
            return trapezoidal_rule(sf, x0, dt, t0, jac, return_derivatives=jac is not None)

    elif integration_method == 'midpoint' or integration_method == 'midpoint-method':
        def create_integration_series(x0):
            return midpoint_method(sf, x0, dt, t0, jac, return_derivatives=jac is not None)

    elif integration_method == 'custom':
        def create_integration_series(x0):
            return numerical_integration_iterator(sf, x0, dt, t0, jac)

    else:
        raise ValueError(f'unknown integration method: {integration_method}')

    def f(x0):
        method = create_integration_series(x0)

        if jac is None:
            y = nth(method, steps) - x0
            return y
        else:
            vals, d = zip(*take(steps, method))
            y = vals[-1] - x0
            j = prod(d) - np.identity(len(y))
            return y, j

    result = root(f, x0, jac=jac is not None).x

    return result
