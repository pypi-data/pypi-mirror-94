from itertools import count

import numpy as np
from scipy.optimize import root

from scipy_steadystate.itertools import nth, take
from scipy_steadystate.numerics import prod
from .backward_euler import backward_euler
from .forward_euler import forward_euler
from .midpoint_method import midpoint_method
from .runge_kutta_method import runge_kutta_method
from .trapezoidal_rule import trapezoidal_rule


def envelope_following_method(f, x0, T, s, m, t0=0, jac=None, skip_method='backward-euler', integration_method='forward-euler'):
    """
    An implementation of the Envelope-Following method (EF-method).

    For reference, see the paper at https://ieeexplore.ieee.org/document/4342106.

    :param f:
        State equation.
    :param x0:
        Initial state condition.
    :param T:
        Period T of the underlying high-frequency component.
    :param s:
        Count of interval integration steps for one EF-step. Used for the integration between `x[0]` -> `x[1]` and
        `x[m-1]` -> `x[m]`.
    :param m:
        Period skip count. Skips `m * T` periods for each EF-step. Must be 3 or greater.
    :param t0:
        Initial time to start solving at.
    :param jac:
        The jacobian of the state equation `f`. Takes two arguments `t` and `x`.
    :param skip_method:
        The skipping method of the EF-method. Constraints how to extrapolate the EF-step for `x[m-1]` and thus `x[m]`.
        Supported methods are:
        - `backward-euler`: x[m] = x[0] + m * (x[m] - x[m-1])
        - `trapezoidal`/`trapezoidal-rule`: x[m] = x[0] + m/2 * (x[1] - x[0] + x[m] - x[m-1])
    :param integration_method:
        The integration method to perform inside a single EF-step. Supported values are:
        - `euler`/`forward-euler`: Performs the most simple form of integration: x2 = x1 + dt * sf(t, x1)
        - `backward-euler`: Simplest implicit integration method: x2 = x1 + dt * sf(t+dt, x2)
        - `trapezoidal`/`trapezoidal-rule`: Trapezoidal rule which averages the value between the current and next step:
          x2 = x1 + dt / 2 * (sf(t, x1) + sf(t+dt, x2))
        - `midpoint`/`midpoint-method`: Midpoint method that uses the value between the current and next step:
          x2 = x1 + dt * sf(t+dt/2, (x1+x2)/2)
    :return:
        An iterator yielding values of the envelope points of the state function `f`.
    """
    if m < 3:
        raise ValueError('m must be 3 or greater (otherwise no meaningful skips would be performed)')

    dt = T / s

    # Notations:
    # x_k0 := x[k]
    # x_k1 := x[k+1]
    # x_km1 := x[k+m-1]
    # x_km0 := x[k+m]

    if skip_method == 'backward-euler':
        def efstep(x_k0, x_k1, x_km1, x_km0):
            return x_k0 + m * (x_km0 - x_km1) - x_km0

        def efstep_jac(integrator_jac):
            return (m - 1) * integrator_jac - m * np.identity(len(x0))

    elif skip_method == 'trapezoidal' or skip_method == 'trapezoidal-rule':
        def efstep(x_k0, x_k1, x_km1, x_km0):
            return x_k0 + 0.5 * m * (x_k1 - x_k0 + x_km0 - x_km1) - x_km0

        def efstep_jac(integrator_jac):
            return 0.5 * m * (integrator_jac - np.identity(len(x0))) - integrator_jac

    else:
        raise ValueError(f'unsupported skip method: {skip_method}')

    if integration_method == 'forward-euler' or integration_method == 'euler':
        def create_integration_series(x0, t0, return_derivatives=False):
            return forward_euler(f, x0, dt, t0, jac, return_derivatives)

    elif integration_method == 'runge-kutta-method' or integration_method == 'runge-kutta' or integration_method == 'rk4':
        def create_integration_series(x0, t0, return_derivatives=False):
            return runge_kutta_method(f, x0, dt, t0, jac, return_derivatives)

    elif integration_method == 'backward-euler':
        def create_integration_series(x0, t0, return_derivatives=False):
            return backward_euler(f, x0, dt, t0, jac, return_derivatives)

    elif integration_method == 'trapezoidal' or integration_method == 'trapezoidal-rule':
        def create_integration_series(x0, t0, return_derivatives=False):
            return trapezoidal_rule(f, x0, dt, t0, jac, return_derivatives)

    elif integration_method == 'midpoint' or integration_method == 'midpoint-method':
        def create_integration_series(x0, t0, return_derivatives=False):
            return midpoint_method(f, x0, dt, t0, jac, return_derivatives)

    else:
        raise ValueError(f'unsupported integration method: {integration_method}')

    x_k0 = x0
    t = t0
    for step in count():
        x_k1 = nth(create_integration_series(x_k0, t), s)

        def efstep_eq(x_km1):
            t_km1 = t + (m-1) * T

            if jac is None:
                integrator = create_integration_series(x_km1, t_km1)
                x_km0 = nth(integrator, s)
                val = efstep(x_k0, x_k1, x_km1, x_km0)

                return val
            else:
                integrator = create_integration_series(x_km1, t_km1, return_derivatives=True)
                integrated, d = zip(*take(s, integrator))
                x_km0 = integrated[-1]
                val = efstep(x_k0, x_k1, x_km1, x_km0)

                integrator_jac = prod(d)
                efstep_eq_jac = efstep_jac(integrator_jac)

                return val, efstep_eq_jac

        # Perform a fast single forward Euler step up to x[k+m-1] to get an initial estimate.
        initial_guess = x_k1 + (m - 2) * (x_k1 - x_k0)
        result = root(efstep_eq, initial_guess, jac=jac is not None).x

        t = t0 + step * m * T
        x_k0 = result

        yield result
