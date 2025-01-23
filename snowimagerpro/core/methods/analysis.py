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

from copy import copy
from pathlib import Path

import cv2 as cv
import numpy as np

from .. import _GLOBALS
from . import _rho as FARRELL

ROOT = _GLOBALS.ROOT

# ROOT = "." #### HOW TO SET THIS MORE GENERALLY?


def apply_SSA(R, wavelength, pix2mm, offset_z=0):
    """Apply SSA conversion. Same as TARTES."""

    rho_i = 916.7  # kg/m3

    ## -- SnowTARTES parameters for sphere -- ##
    g = 0.895
    gG = 2 * g - 1
    B = 1.25

    angle = 45
    mu_0 = np.cos(np.deg2rad(angle))

    lam = wavelength * 1e-9
    n_r = np.loadtxt(
        Path("snowimagerpro/core/calibration/IOP_2008_ASCIItable.dat"), skiprows=1
    )
    idx = np.argmin(np.abs(n_r[:, 0] - lam / 1e-9 / 1000))
    xi = n_r[idx, 2]

    x = 3 / 7 * (1 + 2 * mu_0)
    gamma = 4 * np.pi * xi / lam  # 1/m

    frame_size_x = 50 / pix2mm
    frame_size_y = 30 / pix2mm

    x_size, y_size, extent = image_size(R, pix2mm, offset_z)

    R_framed = frame_image(copy(R), frame_size_x, frame_size_y, x_size)

    def calc_SSA(_R_framed):
        return B * gamma / (3 * rho_i * (np.log(_R_framed) / (8 * x)) ** 2 * (1 - gG))

    SSA = calc_SSA(R_framed)

    _R_cal = np.linspace(0, 1, 100)
    _SSA_cal = calc_SSA(_R_cal)

    # set unrealistic values to zero
    SSA[SSA > 150] = 0
    SSA[SSA < 0] = 0

    sigma = [2, 5]
    # SSA = filters.gaussian(SSA, sigma, mode="constant")
    SSA = cv.GaussianBlur(SSA, (7, 3), 0)

    SSA_profile = np.nanmean(SSA, axis=1)

    return SSA, R_framed, SSA_profile, (_R_cal, _SSA_cal)


def get_density(R, Rprime, SSA_, pix2mm):
    offset_z = 0  # R_meta.offsets

    frame_size_x = 50 / pix2mm
    frame_size_y = 30 / pix2mm

    x_size, y_size, extent = image_size(R, pix2mm, offset_z)

    R_framed = frame_image(copy(R), frame_size_x, frame_size_y, x_size)
    SSA_framed = frame_image(copy(SSA_), frame_size_x, frame_size_y, x_size)
    Rprime_framed = frame_image(copy(Rprime), frame_size_x, frame_size_y, x_size)

    sigma = [2, 5]
    # Rprime_framed = filters.gaussian(Rprime_framed, sigma, mode="constant")
    Rprime_framed = cv.GaussianBlur(Rprime_framed, (7, 3), 0)

    print(f"shape of {R_framed.shape}")
    print(f"shape of {Rprime_framed.shape}")

    masks = generate_slit_masks(Rprime_framed, R_framed.shape[1])
    masks_prime = generate_slit_masks(Rprime_framed, Rprime_framed.shape[1])

    R_masked = mask_images(R_framed, masks)
    SSA_masked = mask_images(SSA_, masks)
    for_rho_masked = mask_images(Rprime_framed, masks_prime)

    SSA_profiles_at_slits = make_profiles(SSA_masked, extent)
    for_rho_profiles_at_slits = make_profiles(for_rho_masked, extent)

    ___rd = [25, 20, 15, 25]

    tmp = []
    for i in range(4):  # TODO: Adjust to number of slits when stitching sideways
        r = ___rd[i]

        _ssa = SSA_profiles_at_slits[i]["value"]

        d_opt = 6 / (_ssa[::1]) / 1000

        ###### rescaling !!!!
        tmp.append(
            FARRELL.phi(for_rho_profiles_at_slits[i]["value"], d_opt, 0.5 * r) - 0.35
        )

    cal_func = FARRELL.phi

    return tmp, SSA_framed, R_masked, for_rho_masked, cal_func


def image_size(image, pix2mm, offset_z):
    x_size = image.shape[1]
    y_size = image.shape[0]
    if -offset_z > 0:
        extent = (0, x_size * pix2mm, -(y_size * pix2mm + offset_z), -offset_z)
    else:
        extent = (0, x_size * pix2mm, 14, y_size * pix2mm + offset_z)

    return x_size, y_size, extent


def frame_image(image, frame_x, frame_y, x_size, frame_value=np.nan):
    x_frame = int(frame_x * x_size)
    y_frame = int(frame_y * x_size)

    x_frame = int(frame_x)
    y_frame = int(frame_y)

    image[:, :x_frame] = frame_value
    image[:, -x_frame:] = frame_value
    image[:y_frame, :] = frame_value
    image[-y_frame:, :] = frame_value

    return image


def generate_slit_masks(img_gri, x_size):
    # --- determine slit parameters --- #
    x0, w0 = get_slit_params_from_image(img_gri, [0, 1, 2, 3], debug=False)
    xx0 = [x * x_size for x in x0]
    ww0 = [w * x_size for w in w0]

    masks = []
    for x0, w0 in zip(xx0, ww0):
        print("x0, w0")
        print(x0, w0)
        masks.append(square_function(np.arange(x_size), x0=[x0], w0=[w0]))

    return masks


def get_slit_params_from_image(img, slits, debug=False):
    img = np.nan_to_num(img)
    if len(np.shape(img)) == 3:
        img = np.mean(img, axis=2)
    img = np.mean(img, axis=0)  # - 0.35
    x_size = np.shape(img)[0]

    cut_value = np.max(img) / 4 * 2

    if debug:
        fig, ax = plt.subplots()
        ax.plot(img)
        ax.axhline(cut_value, color="r")

    indices = [
        idx
        for idx in range(0, len(img) - 1)
        if img[idx] > cut_value
        and img[idx + 1] < cut_value
        or img[idx] < cut_value
        and img[idx + 1] > cut_value
    ]

    indices = [(indices[sel * 2], indices[sel * 2 + 1]) for i, sel in enumerate(slits)]
    x0 = [(low + high + 2) / 2 / x_size for low, high in indices]
    w0 = [(high - low + 1) / x_size for low, high in indices]

    if debug:
        ax.scatter(
            [x * x_size for x in x0], [cut_value] * len(x0), marker="x", color="r"
        )
        for i in range(len(x0)):
            ax.axvline((x0[i] - w0[i] / 2) * x_size, color="r", linestyle="--")
            ax.axvline((x0[i] + w0[i] / 2) * x_size, color="r", linestyle="--")

    return x0, w0


def square_function(x, x0, w0):
    """Square function at rel. position x0 and rel. width w0."""

    # x0 = [_x0 * len(x) for _x0 in x0]
    # w0 = [_w0 * len(x) for _w0 in w0]

    # x0 = [_x0 for _x0 in x0]
    # w0 = [_w0 for _w0 in w0]

    S = np.zeros(len(x))

    for _x0, _w0 in zip(x0, w0):
        S += square(x, x0=_x0, width=_w0)

    return S


def square(x, x0=0, width=10):
    """Make square wave function."""
    y = []

    for x in x:
        if x0 - width / 2 <= x <= x0 + width / 2:
            y.append(1)
        else:
            y.append(0)
    return y


def mask_image(image, mask):
    image = image * mask
    image[image == 0] = np.nan

    return image


def mask_images(image, masks):
    masked_images = []
    for mask in masks:
        masked_images.append(mask_image(image, mask))

    return masked_images


def make_profile(image, extent):
    value = np.nanmean(image, axis=1)
    height = np.linspace(extent[2], extent[3], len(value))
    # image y coordinates are flipped !

    profile = {"height": height[::-1], "value": value[::1]}

    return profile


def make_profiles(images, extent):
    profiles = []

    for image in images:
        profile = make_profile(image, extent)
        profiles.append(profile)

    return profiles
