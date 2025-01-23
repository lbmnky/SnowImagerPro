#
# This file is part of SnowImagerPro (https://github.com/lbmnky/SnowImagerPro).
#
# Copyright (C) 2025 Lars Mewes
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.
#

import numpy as np
from scipy.special import lambertw as lambertw_scipy

from snowimagerpro.core.methods.lambertw import lambert_w as lambertw

# physical constants
kappa_ice = 0.0027  # 0.0027 / mm-1
rho_ice = 917  # 917 / kg/m-3
g = 0.85  # 0.85

# parameters
A = 1.26  # 1.26
B = 0.79  # 0.79


def phi(R, d_opt, r):
    r"""$\phi_{\rho, d_\mathrm{opt}}(R)$"""

    # Need to solve z = 1/x * (e^(x))^-a for x
    # x = W(a/z)/a

    global kappa_ice
    global A
    global B
    global g

    C = _C(d_opt)
    const = _const(d_opt)

    _a = A * np.sqrt(3 * kappa_ice * C)
    _z = (R + const) / (kappa_ice / C - 1) * C / B

    _x = lambertw(_a / _z, 0, 0) / _a

    phi = 1 / r * np.sqrt(_x**2 - (B**2 / C**2))

    phi[np.iscomplex(phi)] = np.nan

    return np.real(phi)  # VALID VIA COMPARISON TO SCIPY ::: #TODO: REMOVE def phi_scipy


def phi_scipy(R, d_opt, r):
    r"""$\phi_{\rho, d_\mathrm{opt}}(R)$"""

    # Need to solve z = 1/x * (e^(x))^-a for x
    # x = W(a/z)/a

    global kappa_ice
    global A
    global B
    global g

    C = _C(d_opt)
    const = _const(d_opt)

    _a = A * np.sqrt(3 * kappa_ice * C)
    _z = (R + const) / (kappa_ice / C - 1) * C / B

    _x = lambertw_scipy(_a / _z) / _a

    phi = 1 / r * np.sqrt(_x**2 - (B**2 / C**2))

    phi[np.iscomplex(phi)] = np.nan

    return np.real(phi)


# MORE AUX FUNCTIONS
def _const(d_opt):
    """Constant offset in integral (R_truncated_Greens_func) that ensures that the integral is
    zero when evaluated at  r = 0."""

    global kappa_ice
    global A
    global B
    global g

    C = _C(d_opt)

    return (kappa_ice / C - 1) * np.exp(-A * np.sqrt(3 * kappa_ice * B**2 * C ** (-1)))


def _C(d_opt):
    """Constant in integral (R_truncated_Greens_func) that depends on d_opt."""

    global kappa_ice
    global g
    global A
    global B

    return kappa_ice + 0.84 / A * (1 - g) * np.sqrt(kappa_ice / d_opt)
