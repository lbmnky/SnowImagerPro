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

import csv
import json
import logging
import time
from copy import deepcopy
from pathlib import Path
from typing import Union

import cv2 as cv
import numpy as np
from pydantic import ValidationError

from snowimagerpro.core._GLOBALS import ROOT, globals

from ..metadata import ImageMetadata
from .helper import error_msg
from .image_loading import load_bayer, load_dng, load_dng_preview



def load_db(_db_path):
    """
    Load a database from the given file path.
    Args:
        _db_path (str): The path to the database file.
    Returns:
        dict: A dictionary containing the loaded image database.
    Raises:
        SyntaxError: If there is a syntax error while loading the database.
    """

    logging.info(f"loading db from {_db_path}")

    try:
        with open(_db_path) as data_file:
            reader = csv.DictReader(data_file)

            image_db = {}
            for row in reader:
                try:
                    meta = ImageMetadata(**row)
                except ValidationError as e:
                    print(json.dumps(e.errors(), indent=4))
                image_db[meta.ID] = meta

    except SyntaxError as error:
        logging.info("failed to load database (init_tree).")
        logging.info(error)

    return image_db


def load_image(fp):
    """
    Load an image file and return the data and EXIF metadata.
    Args:
        fp (str): The file path of the image file.
    Returns:
        tuple: A tuple containing the image data and EXIF metadata.
    Raises:
        None
    """

    ext = fp.suffix[1:]
    if ext == "bay":
        logging.info("load single .bay image")
        _data, _exif = load_bayer(fp)
    elif ext == "dng":
        logging.info("load single .dng image")
        _data, _exif = load_dng(fp)
    elif ext == "RAW":
        logging.info("load single .raw image")
        # TODO: load RAW from MOSAiC
        pass
    else:
        logging.info(f"File with extension {ext} is not a valid image file.")

    return _data, _exif


def load_preview(fp):
    """
    Load a preview image from the given file path.
    Parameters:
    - fp (str): The file path of the image file.
    Returns:
    - _out (ndarray or None): The loaded image as a NumPy array, or None if the file is not a valid image file.
    - None: This function always returns None as the second value.
    """

    ext = fp.suffix[1:]

    if ext == "bay":
        _out, _ = load_bayer(fp, shrink=1)
        _out = _out[:, :, 0]
    elif ext == "dng":
        _out, _ = load_dng_preview(fp)
    else:
        logging.info(f"File with extension {ext} is not a valid image file.")
        _out, _ = None, None

    return _out, None


def check_image_db(image_db):
    IDs = [int(i.ID) for i in image_db]

    s = np.sort(IDs, axis=None)

    if (s[1:] == s[:-1]).any():
        logging.info("Bad! IDs are not unique.")
        logging.info(s)
    else:
        logging.info("Good! IDs are unique.")


def average_in_ROI(img, ROI):
    img = np.atleast_3d(img)

    size = get_img_size(img)

    avs = []

    for roi in ROI:
        (x0, y0), (x1, y1) = rel2pix(roi, size)
        avs.append(list(np.nanmean(np.nanmean(img[y0:y1, x0:x1], axis=0), axis=0)))

    return avs


def ROI_pos_to_size(roi, size):
    (width, height) = size

    if len(roi) == 2:
        x = roi[0][0] * width
        y = roi[0][1] * height

        width = roi[1][0] * width - x
        height = roi[1][1] * height - y

    if len(roi) == 4:
        x = roi[0][0] * width
        y = roi[0][1] * height

        width = roi[2][0] * width - x
        height = roi[2][1] * height - y

    return (x, y), (width, height)


def get_img_size(img) -> list | None:
    """Get the x,y dimensions of an image."""

    if img.__class__.__name__ == "Image":
        return [len(img._data[0]), len(img._data)]
    elif isinstance(img, np.ndarray):
        return [len(img[0]), len(img)]
    else:
        error_msg("img must be of type Image or np.ndarray")
        return None


def rel2pix(relative_position, image_size):
    """Convert relative position to pixels."""
    return [
        [round(r * s) for r, s in zip(rel, image_size)] for rel in relative_position
    ]


def transform_image(img, src, dst, type="projective"):
    """Transform image using skimage.transform."""

    img_size = get_img_size(img)

    src = np.array(src) * img_size
    dst = np.array(dst) * img_size

    if type == "projective":
        tform3 = transform.ProjectiveTransform()
    elif type == "similarity":
        tform3 = transform.SimilarityTransform()
        A = np.concatenate((src, [(0, 0)]))
        B = np.concatenate((dst, [(0, 0)]))

        # tform = cv.getAffineTransform(A, B) # TODO: replace skimage with cv2 and check if faster

    elif type == "affine":
        tform3 = transform.AffineTransform()
    else:
        raise ValueError("Transformation type not supported.")

    tform3.estimate(src, dst)

    img._data = transform.warp(img._data, tform3.inverse)

    return img


def undistort_image(img):
    """Undistort image using cv2.undistort."""

    with open(ROOT / Path("distortion_calib.json")) as f:
        dist = json.load(f)

    camera_matrix = np.array(dist["camera_matrix"])
    distortion_coeff = np.array(dist["distortion_coeff"])

    img._data = cv.undistort(img._data, camera_matrix, distortion_coeff, None)
    return img


def shift_image(M, dy, dx):
    """Use padding to shift and expand image."""
    if dx != 0:
        M = shift_x(M, dx)
    if dy != 0:
        M = shift_y(M, dy)
    return M


def shift_y(M, dy):
    if dy >= 0:
        _pad = ((dy, 0), (0, 0))
    else:
        _pad = ((0, -dy), (0, 0))

    M = np.pad(M, _pad, mode="constant", constant_values=0)
    logging.info(f"shifting in y-direction by: {-dy}")
    return M


def shift_x(M, dx):
    if dx >= 0:
        _pad = ((0, 0), (dx, 0))
    else:
        _pad = ((0, 0), (0, -dx))

    M = np.pad(M, _pad, mode="constant", constant_values=0)
    logging.info(f"shifting in x-direction by: {-dx}")
    return M


def coords_mm_to_pix_OBSOLETE(images):
    """Use image coordinates to position (not place) images on super-image.

    Write position to img._pos

    """

    y_max = 0
    x_min = 0

    for key, img in images.items():
        img_size = get_img_size(img)

        coords_pix = [int(a * b) for a, b in zip(img._meta.coords_pix, img_size)]

        coords_mm = img._meta.coords_mm

        px_2_mm = img._meta.px_2_mm

        coords_mm_in_pix = [int(a / px_2_mm) for a in coords_mm]

        y_max = coords_mm_in_pix[1] if coords_mm_in_pix[1] > y_max else y_max
        x_min = (
            coords_mm_in_pix[0] - coords_pix[0]
            if coords_mm_in_pix[0] - coords_pix[0] < x_min
            else x_min
        )

        coords_mm_in_pix = (coords_mm_in_pix[0] - coords_pix[0], coords_mm_in_pix[1])
        img._pos = coords_mm_in_pix

    for key, img in images.items():
        coords_mm_in_pix = img._pos
        coords_mm_in_pix = (coords_mm_in_pix[0] - x_min, y_max - coords_mm_in_pix[1])
        img._pos = coords_mm_in_pix

    return images


def coords_mm_to_pix(images):
    """

    (x_0,y_0)
      +---------------------+
      |                     |
      |                     |
      |       (x,y)         |
      |      +              |
      |                     |
      +---------------------+

      (x_0, y_0) : origin
      (x, y) : reference position

      return origin in mm

    """

    offset = [np.inf, np.inf]

    for img in images.values():
        img_size = get_img_size(img)
        pix_pos = [int(a * b) for a, b in zip(img._meta.coords_pix, img_size)]
        mm_pos = img._meta.coords_mm
        scale = img._meta.px_2_mm

        origin_mm = [
            float(mm_pos[0] + pix_pos[0] * scale),
            float(mm_pos[1] + pix_pos[1] * scale),
        ]

        if origin_mm[0] < offset[0]:
            offset[0] = origin_mm[0]
        if origin_mm[1] < offset[1]:
            offset[1] = origin_mm[1]

        img._pos = origin_mm

    # subtract smallest x,y position from all images
    for img in images.values():
        img._pos = [img._pos[0] - offset[0], img._pos[1] - offset[1]]

    return images


def image_sorting(images):
    _out = {
        "ngr": {},
        "gri": {},
    }

    for item in images.items():
        key, img = item
        _out[img._meta.img_type][key] = img

    """ #TODO: Implement sorting into groups by coordinates

    """

    return _out


def image_registration_col_major(images):
    pass


def image_registration_row_major(images):
    pass


def image_registration(current_image, super_image, dx, dy):
    """
    Aligns the current image with the super image by shifting the images horizontally and vertically.
    Args:
        current_image (ndarray): The current image to be aligned.
        super_image (ndarray): The super image to be aligned with.
        dx (int): The horizontal shift value.
        dy (int): The vertical shift value.
    Returns:
        Tuple[ndarray, ndarray]: A tuple containing the aligned current image and the aligned super image.
    """

    current_image = shift_image(current_image, -dy, dx)

    # adjust super-image shape
    if super_image.shape[1] < current_image.shape[1]:
        _dx = current_image.shape[1] - super_image.shape[1]
        super_image = shift_x(super_image, -(2 * (dx >= 0) - 1) * np.abs(_dx))
    elif super_image.shape[1] > current_image.shape[1]:
        _dx = super_image.shape[1] - current_image.shape[1]
        current_image = shift_x(current_image, -(2 * (dx >= 0) - 1) * np.abs(_dx))

    if super_image.shape[0] < current_image.shape[0]:
        _dy = current_image.shape[0] - super_image.shape[0]
        super_image = shift_y(super_image, +(2 * (dy >= 0) - 1) * np.abs(_dy))
    elif super_image.shape[0] > current_image.shape[0]:
        _dy = super_image.shape[0] - current_image.shape[0]
        current_image = shift_y(current_image, +(2 * (dy >= 0) - 1) * np.abs(_dy))

    return current_image, super_image


def find_overlap_mask(ma_A, ma_B, sigmaX, sigmaY) -> np.ndarray:
    """
    Calculates the overlap mask between two input masks.
    Args:
        ma_A (np.ndarray): The first input mask.
        ma_B (np.ndarray): The second input mask.
        sigmaX (float): The standard deviation in the X direction.
        sigmaY (float): The standard deviation in the Y direction.
    Returns:
        np.ndarray: The overlap mask between ma_A and ma_B.
    """

    _mask = ma_A + ma_B
    _size = _mask.shape
    sigma = np.sqrt(sigmaX**2 + sigmaY**2)

    # TODO: Improve performance by selecting region "around" the new mask ... won't get rid of the following:

    __size = _size

    # TODO: Seems faster but artefacts at corners of images
    # TODO: col-major and row-major blending implementation to avoid artefacts

    scale = 20
    __mask = _mask[::scale, ::scale]
    sigma = sigma / scale**1  # TODO: find optimal rescale factor
    sigmaX = sigmaX / scale**1
    sigmaY = sigmaY / scale**1

    _kernel = (4 * int(sigmaX) + 1, 4 * int(sigmaY) + 1)
    __mask = cv.GaussianBlur(__mask, _kernel, sigmaX=sigmaX, sigmaY=sigmaY)
    _mask = cv.resize(__mask, None, fx=scale, fy=scale)

    if _mask.shape != __size:
        logging.info("mask resize")
        _mask = cv.resize(_mask, (__size[1], __size[0]))

    # test = ma_A - ma_B
    # test = ma_B
    # test[test > 0] = 1
    # _mask = np.array(_mask[:, :]) * test  ### TODO: sharper edges where no overlap?

    _mask = _mask.round(5)
    _mask = 1 - np.greater(_mask, 0).astype(np.uint8)
    _mask[np.where(ma_B == 0)] = 0

    box = bbox(_mask)
    _mask[box[0] : box[1], box[2] : box[3]] = 1

    return _mask


def Gaussian(size, fwhm):
    sigma = fwhm / 2.355
    x = np.arange(-size // 2 + 1, size // 2 + 1)
    y = np.arange(-size // 2 + 1, size // 2 + 1)
    x, y = np.meshgrid(x, y)
    g = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    return g / g.sum()


def Lorentzian(size, fwhm):
    gamma = fwhm / 2
    x = np.arange(-size // 2 + 1, size // 2 + 1)
    y = np.arange(-size // 2 + 1, size // 2 + 1)
    x, y = np.meshgrid(x, y)
    out = gamma / (x**2 + y**2 + gamma**2)
    return out / out.sum()


def Square(size, fwhm):
    s = np.zeros((size, size))
    s[size // 4 : 3 * size // 4, size // 4 : 3 * size // 4] = 1
    return s


def bbox(img):
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return rmin, rmax, cmin, cmax


def find_overlap_mask_by_shape(ma_A, ma_B, sigma):
    pass


def image_blending(
    images, algo="laplPyr", sigmaX=100, sigmaY=100
) -> tuple[np.ndarray, Union[list, None], Union[list, None]]:
    # collect metadata of individual images
    meta = [(k, v._meta.__dict__) for k, v in images.items()]
    exif = [(k, v._exif) for k, v in images.items()]

    images = deepcopy(images)  # avoid rotation when processing several times

    for _img in images.values():
        t = time.time()
        # transform image if necessary
        src = _img._meta.trafo_points
        if len(src) == 2:
            src_dx = src[1][0] - src[0][0]
            x_new = src[0][0] + src_dx / 2
            dst = [[x_new, src[0][1]], [x_new, src[1][1]]]
            # if src != dst:
            # _img = transform_image(_img, src, dst, type="similarity") ###### TODO: temporary remove rotation correction
            # _img = undistort_image(_img)
            print(f"transforming image took {time.time() - t}")

    if algo == "laplPyr":
        return image_blending_laplPyr(images, sigmaX, sigmaY), meta, exif
    elif algo == "off":
        return image_blending_off(images), meta, exif
    else:
        return np.zeros((1, 1)), None, None


def image_blending_off(images):
    super_image: np.ndarray = np.zeros((1, 1))

    for i, key in enumerate(images.keys()):
        try:  # TODO: Improve handling of single and three channel images
            current_image = np.mean(images[key]._data, axis=2)
        except Exception:
            current_image = images[key]._data

        dx, dy = images[key]._pos

        print(
            f"image of type {images[key]._meta.img_type} and with id {key} "
            f"has position {dx}, {dy}"
        )

        current_image, super_image = image_registration(
            current_image, super_image, dx, dy
        )

        if i > 0:
            super_image += current_image
        else:
            super_image = current_image

    super_image[np.where(super_image > 1)] /= 2
    super_image[np.where(super_image > 1)] /= 2

    return super_image


def image_blending_linGrad(images):
    pass


def image_blending_laplPyr(images, sigmaX=100, sigmaY=100) -> np.ndarray:
    """Blend images.

    First blend images by column, then by row, or vice versa.
    Fastest way so far is reduce size of image, filter and upscale.

    Too slow:
    - Gaussian smoothing with "large" kernel (`cv.GaussianBlur(ma_A, _kernel, sigma`)
    - for-loop with linear Gaussian smoothing filter in x- and y-dimension
    - Laplacian pyramid of mask
    - FFT filtering

    Too fiddly:
    - finding center of mass and shape of mask

    """
    image: np.ndarray = np.zeros((1, 1))

    images = convert_to_grayscale(images)

    masks = []

    for i, _img in enumerate(images.values()):
        dx_mm, dy_mm = _img._pos
        scale = _img._meta.px_2_mm
        dx = int(dx_mm / scale)
        dy = int(dy_mm / scale)

        print(_img._meta.filepath)
        print("dx_mm, dy_mm", dx_mm, dy_mm)
        print("dx, dy", dx, dy)

        t = time.time()
        _data, image = image_registration(_img._data, image, dx, dy)
        logging.info(f"Alignment in {time.time() - t} sec")

        if i > 0:
            t = time.time()
            mask, crop = _mask(image, _data, sigmaX, sigmaY)
            masks.append(mask)  ### TODO: mask parameters for reusability
            logging.info(f"Masking in {time.time() - t} sec")

            t = time.time()
            image = _laplPyr_blend(image, _data, mask, crop)
            logging.info(f"Blending in {time.time() - t} sec")

            if globals.DEBUG:
                rmin, rmax, cmin, cmax = crop
                _tmp = np.zeros_like(image)
                _tmp[rmin:rmax, cmin:cmax] = mask
                m = _tmp
                ___mask = (m - np.roll(m, 5, axis=0)) + (m - np.roll(m, 5, axis=1))
                ___mask[___mask > 0] = 1

                stitching_line_img = np.zeros_like(image) + ___mask

        else:
            image = _data
            stitching_line_img = np.zeros_like(image)

        if globals.DEBUG:
            image += stitching_line_img

    return image


def _mask(image_A, image_B, sigmaX, sigmaY):
    ma_A = deepcopy(image_A)
    ma_B = deepcopy(image_B)

    ma_A[image_A != 0] = 1
    ma_B[image_B != 0] = -1
    # HINT: A and B can have negative values after bg subtraction, etc ...

    _size = image_A.shape
    rmin, rmax, cmin, cmax = bbox(ma_B)
    rmin = int(rmin * 0.9)
    cmin = int(cmin * 0.9)

    if rmax * 1.1 < _size[0]:
        rmax = int(rmax * 1.1)
    else:
        rmax = _size[0]

    if cmax * 1.1 < _size[1]:
        cmax = int(cmax * 1.1)
    else:
        cmax = _size[1]

    image_A = image_A[rmin:rmax, cmin:cmax]
    image_B = image_B[rmin:rmax, cmin:cmax]

    ma_A = ma_A[rmin:rmax, cmin:cmax]
    ma_B = ma_B[rmin:rmax, cmin:cmax]

    mask = find_overlap_mask(ma_A, ma_B, sigmaX, sigmaY)

    return mask, [rmin, rmax, cmin, cmax]


def _laplPyr_blend(image_A, image_B, mask, crop):
    rmin, rmax, cmin, cmax = crop

    orig_A = deepcopy(image_A)
    image_A = image_A[rmin:rmax, cmin:cmax]
    image_B = image_B[rmin:rmax, cmin:cmax]

    pyrLvls = 6

    # generate Gaussian pyramid for A
    G = image_A.copy()
    gpA = [G]
    for i in range(pyrLvls):
        G = cv.pyrDown(G)
        gpA.append(G)

    # generate Gaussian pyramid for B
    G = image_B.copy()
    gpB = [G]
    for i in range(pyrLvls):
        G = cv.pyrDown(G)
        gpB.append(G)

    # generate Gaussian pyramid for mask
    G = mask.copy()
    gpM = [G]
    for i in range(pyrLvls):
        G = cv.pyrDown(G)
        gpM.append(G)

    # generate Laplacian Pyramid for A
    lpA = [gpA[pyrLvls - 1]]
    for i in range(pyrLvls - 1, 0, -1):
        size = (gpA[i - 1].shape[1], gpA[i - 1].shape[0])
        GE = cv.pyrUp(gpA[i], dstsize=size)
        L = cv.subtract(gpA[i - 1], GE)
        lpA.append(L)

    # generate Laplacian Pyramid for B
    lpB = [gpB[pyrLvls - 1]]
    for i in range(pyrLvls - 1, 0, -1):
        size = (gpB[i - 1].shape[1], gpB[i - 1].shape[0])
        GE = cv.pyrUp(gpB[i], dstsize=size)
        L = cv.subtract(gpB[i - 1], GE)
        lpB.append(L)

    # reverse mask
    gpMr = [gpM[pyrLvls - 1]]
    for i in range(pyrLvls - 1, 0, -1):
        gpMr.append(gpM[i - 1])

    # Now add masked images
    LS = []
    for la, lb, gm in zip(lpA, lpB, gpMr):
        gm = 1 - gm
        ls = la * gm + lb * (1.0 - gm)
        LS.append(ls)

    # now reconstruct
    ls_ = LS[0]
    for i in range(1, pyrLvls):
        size = (LS[i].shape[1], LS[i].shape[0])
        ls_ = cv.pyrUp(ls_, dstsize=size)
        ls_ = cv.add(ls_, LS[i])

    orig_A[rmin:rmax, cmin:cmax] = ls_
    image_A = orig_A

    return image_A


def convert_to_grayscale(images) -> dict:
    """Convert images to grayscale."""
    # TODO: Improve handling of different image types

    for _img in images.values():
        try:
            _img._data = np.mean(_img._data, axis=2)
        except Exception:
            print("gray image already")

    return images


def get_sn(exif) -> str:
    if exif is not None:
        try:
            sn = str(exif["Image BodySerialNumber"])
        except Exception as e:
            print(e)
            try:
                sn = exif["metadata"]["device"]
            except Exception as e:
                print(e)

    else:
        sn = "unknown"

    return sn
