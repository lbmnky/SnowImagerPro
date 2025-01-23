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

import logging
import numpy as np
import h5py
import copy
import rawpy
import exifread
import yaml

from pathlib import Path
import snowimagerpro.core.methods.helper as helper


def load_dng(path, shrink=2):
    """Load a DNG file containing the raw image data."""

    with rawpy.imread(str(path)) as raw:
        raw_image = raw.raw_image.copy()

        black_level = raw.black_level_per_channel[0]
        white_level = raw.white_level

    with open(path, "rb") as f:
        exif = exifread.process_file(f)

    image = np.zeros(
        (raw_image.shape[0] // 2, raw_image.shape[1] // 2) + (3,), dtype=np.uint16
    )

    # TODO double check demosaicing pattern with correct camera ... should be alright, starts from bottom left corner!
    image[:, :, 0] = raw_image[1::2, 0::2]  # red channel
    image[:, :, 1] = (
        raw_image[0::2, 0::2] // 2 + raw_image[1::2, 1::2] // 2
    )  # green channel
    image[:, :, 2] = raw_image[0::2, 1::2]  # blue channel

    image = helper.bin_ndarray(
        image, (image.shape[0] // shrink, image.shape[1] // shrink, 3), operation="mean"
    )

    #image = (image - black_level) / (white_level - black_level - 1)
    image = image / white_level

    try:
        metafile = str(path).split("-")[:-1]
        metafile = "-".join(metafile) + "_metadata.yaml"
        with open(metafile, "r") as f:
            metadata = yaml.safe_load(f)

    except Exception as e:
        print(e)
        metadata = {}

    exif = {**exif, **metadata}

    return image, exif

def load_dng_preview(path, shrink=4):
    assert isinstance(path, (str, Path)), "Path must be str or PosixPath!"

    with rawpy.imread(str(path)) as raw:
        try:
            thumb = raw.extract_thumb()
            thumb = thumb.data
        except rawpy.LibRawNoThumbnailError:
            thumb = raw.postprocess(use_camera_wb=True, no_auto_bright=True, output_bps=8, half_size=True, demosaic_algorithm=rawpy.DemosaicAlgorithm.LINEAR)
            thumb = thumb[:, :, ::-1]

    return np.mean(thumb[::shrink, ::shrink], axis=2) / 255, None


def load_hdf5_latest(path, ext="hdf5", shrink=1):

    print(f"Loading HDF5 data with extension: {ext}", end=" ... ")

    with h5py.File(path, "r") as file:
        img_keys = file["SnowImage(s)"].keys()

        image_ngr = file["SnowImage(s)"]["ngr"]["image"][::shrink, ::shrink]

        if "gri" in img_keys:
            image_gri = file["SnowImage(s)"]["gri"]["image"][::shrink, ::shrink]
        else:
            image_gri = None

        try:
            px2mm = file["SnowImage(s)"]["ngr"]["image"].attrs["pix2mm"] * shrink
            reference_pix_xz = file["SnowImage(s)"]["ngr"]["image"].attrs["reference_pix_xz"]
            reference_pos_xz = file["SnowImage(s)"]["ngr"]["image"].attrs["reference_pos_xz"]
        except Exception as e:
            print(e)
            print("backwards compatibility")
            px2mm = file["SnowImage(s)"]["ngr"]["pix2mm"][()] * shrink
            reference_pix_xz = file["SnowImage(s)"]["ngr"]["reference_pix_xz"][()]
            reference_pos_xz = file["SnowImage(s)"]["ngr"]["reference_pos_xz"][()]


        offset_z = []

        aux_data = {}

        aux_data = dict(file["SnowImage(s)"].attrs.items())


        print("\n")
        print(image_ngr.shape[1])
        print(reference_pix_xz)
        if isinstance(reference_pix_xz, np.ndarray):

            h = image_ngr.shape[0] // shrink
            H = h * px2mm
            #W = image_ngr.shape[1] * px2mm

            h0 = reference_pix_xz[1] // shrink
            H0 = h0 * px2mm

            off = H0 - H

            print("Calc. offset")
            print(H)
            print(H0)
            print(off)

            offset_z.append(
                reference_pos_xz[1]
                - (image_ngr.shape[0] - reference_pix_xz[1]) * px2mm
            #    off
            )
        else:
            offset_z.append(0)

        print("Done!")

    images = [[image_ngr], [image_gri]]

    return images, px2mm, offset_z, aux_data

# TODO: ENSURE BACKWARDS COMPATIBILITY
def load_hdf5_latest_(path, ext="hdf5", shrink=1):

    print(f"Loading HDF5 data with extension: {ext}", end=" ... ")

    with h5py.File(path, "r") as file:
        img_keys = file["SnowImage(s)"].keys()

        image_ngr = file["SnowImage(s)"]["ngr"]["image"][::shrink, ::shrink]

        if "gri" in img_keys:
            image_gri = file["SnowImage(s)"]["gri"]["image"][::shrink, ::shrink]
        else:
            image_gri = None

        px2mm = file["SnowImage(s)"]["ngr"]["pix2mm"][()] * shrink

        reference_pix_xz = file["SnowImage(s)"]["ngr"]["reference_pix_xz"][()]
        reference_pos_xz = file["SnowImage(s)"]["ngr"]["reference_pos_xz"][()]

        offset_z = []

        aux_data = {}

        aux_data = dict(file["SnowImage(s)"].attrs.items())


        print("\n")
        print(image_ngr.shape[1])
        print(reference_pix_xz)
        if isinstance(reference_pix_xz, np.ndarray):

            h = image_ngr.shape[0] // shrink
            H = h * px2mm
            #W = image_ngr.shape[1] * px2mm

            h0 = reference_pix_xz[1] // shrink
            H0 = h0 * px2mm

            off = H0 - H

            print("Calc. offset")
            print(H)
            print(H0)
            print(off)

            offset_z.append(
                reference_pos_xz[1]
                - (image_ngr.shape[0] - reference_pix_xz[1]) * px2mm
            #    off
            )
        else:
            offset_z.append(0)

        print("Done!")

    images = [[image_ngr], [image_gri]]

    return images, px2mm, offset_z, aux_data


def load_hdf5(path, ext="hdf5", shrink=2):
    """Load a HDF5 file containing the processed image and auxiliary data."""

    logging.info(f"Loading HDF5 data with extension: {ext}")

    with h5py.File(path, "r") as file:
        img_keys = file["SnowImage"].keys()

        # [()] loads to memory ...
        # nogrid_img = file["SnowImage"][img_key]["no_grid"][()][::shrink, ::shrink]
        # ...

        image = []
        image_ngr = []
        image_gri = []

        px2mm = []
        offset_z = []

        for key in img_keys:
            image_ngr.append(file["SnowImage"][key]["no_grid"][::shrink, ::shrink])
            image_gri.append(file["SnowImage"][key]["grid"][::shrink, ::shrink])

            # image.append(np.hstack((nogrid_img, grid_img)))

            px2mm.append(file["SnowImage"][key]["pix2mm"][()] * shrink)

            reference_pix_xz = file["SnowImage"][key]["reference_pix_xz"][()] // shrink
            reference_pos_xz = file["SnowImage"][key]["reference_pos_xz"][()]

            if isinstance(reference_pix_xz, np.ndarray):
                offset_z.append(
                    reference_pos_xz[1]
                    - (image_ngr[-1].shape[0] - reference_pix_xz[1]) * px2mm[-1]
                )
            else:
                offset_z.append(0)


    images = [image_ngr, image_gri]

    return images, px2mm, offset_z


def load_hdf5_legacy(path, ext):
    """Load a HDF5 file containing the processed image and auxiliary data."""

    print(f"Loading HDF5 data with extension: {ext}", end=" ... ")

    with h5py.File(path, "r") as file:
        nogrid_img = file["image"]["no grid"][()][::4, ::4]
        grid_img = file["image"]["grid"][()][::4, ::4]

    print("Done!")

    image = np.hstack((nogrid_img, grid_img))

    return image


def load_bayer(path, version=None, shrink=1):
    """Loads bayer data."""

    print("Loading Bayer data ", end=" ... ")


    with open(path, "rb") as file:
        data = file.read()

    data = np.fromstring(data, dtype=np.uint8)

    parameters = {
        1: ((1952, 3264), (1944, 3240)),
        2: (
            (2480, 4128),
            (2464, 4100),
        ),  #                  2464, 3280 Cam: v2, Lib: picamera 1, highest resolution
        3: (
            (2464, 4128),
            (2464, 4100),
        ),  # sensor mode 3    2464, 3280 Cam: v2, Lib: Picamera 2, highest resolution
        4: (
            (864, 1536),
            (864, 1536),
        ),  # sensor mode 0     864, 1536 Cam: v3, Lib: Picamera 2
        5: (
            (1296, 2880),
            (1296, 2880),
        ),  # sensor mode 1    1296, 2304 Cam: v3, Lib: Picamera 2
        6: (
            (2592, 5760),
            (2592, 5760),
        ),  # sensor mode 2    2592, 4608 Cam: v3, Lib: Picamera 2, highest resolution
        7: (
            (3040, 6112),
            (3040, 6084),
        ),  #                  3040, 4056 Cam: hq, Lib: Picamera 2, highest resolution
    }

    x_sizes = {
        1: 0,
        2: 3280,
        3: 3280,
        4: 2304,
        5: 2304,
        6: 4608,
        7: 4056,
    }

    if version is None:
        versions = np.arange(1, 8)
    else:
        versions = [version]

    for i, ver in enumerate(versions):
        reshape, crop = parameters[ver]

        try:
            data = data.reshape(reshape)[: crop[0], : crop[1]]
            data = data.astype(np.uint16) << 2

            if ver < 7:
                # five bytes into 4 10-bit values (4 pixels)
                for byte in range(4):
                    data[:, byte::5] |= (data[:, 4::5] >> ((4 - byte) * 2)) & 0b11
                data = np.delete(data, np.s_[4::5], 1)

            elif ver == 7:
                # three bytes into 2 12-bit values (2 pixels)
                for byte in range(2):
                    data[:, byte::3] |= (data[:, 2::3] >> ((2 - byte) * 2)) & 0b11
                data = np.delete(data, np.s_[2::3], 1)

            y_size = parameters[ver][1][0]
            x_size = x_sizes[ver]

            image = np.zeros((y_size // 2, x_size // 2) + (3,), dtype=data.dtype)

        except Exception:
            continue

    image[:, :, 0] = data[1::2, 0::2]  # red channel
    image[:, :, 1] = (data[0::2, 0::2] + data[1::2, 1::2]) // 2  # green channel
    image[:, :, 2] = data[0::2, 1::2]  # blue channel

    # reduce data size for visualization efficiency
    image = image[::shrink, ::shrink]

    print(path)

    try:
        metafile = str(path).split("-")[:-1]
        metafile = "-".join(metafile) + "_metadata.yaml"
        with open(metafile, "r") as f:
            metadata = yaml.safe_load(f)

    except Exception as e:
        print(e)
        metadata = None

    print("Done!")

    return image / 1023, metadata


def load_npy(path, ext):
    """Load data from .npy file.

    Args:
        path (string): _description_
        ext (string): _description_
    """

    print(f"Loading NPY data with extension: {ext}", end=" ... ")
    data = np.load(path)
    print("Done!")

    return data[::2, ::2, :]


def load_rgb(path, ext):
    """Load data from .rgb or .rgba file.

    Supported image sizes are:
    - 3280 x 2464 px^2
    - 3072 x 2304 px^2
    - 1024 x  768 px^2

    Args:
        path (string): _description_
        ext (string): _description_

    Returns:
        _type_: _description_
    """

    print(f"Loading RGB(A) with extension: {ext}", end=" ... ")
    if ext == "rgb":
        channels = 3
    elif ext == "rgba":
        channels = 4
    else:
        print("RGB(A) data can only have 3(4) channels.")

    image = np.fromfile(path, np.dtype("uint8"))
    image_length = int(image.shape[0] / channels)

    # because image dimension is unknown, test
    # x-dimension in decreasing order
    x_dims = [3296, 3280, 3072, 1024]

    for x_dim in x_dims:
        if (image_length % x_dim) == 0:
            y_dim = image_length // x_dim

            if y_dim > 500:  # skip image size with y_dim < 500
                break

    image = image.reshape(y_dim, x_dim, channels)

    if ext == "rgb":
        image = image[::4, ::4]

    print("Done!")

    return image[:, :, :3]


def load_raw(path, ext="RAW"):
    """Load data from .raw file.

    Arguments:
    ----------
    path (string): _description_
    ext (string): _description_

    Returns:
    --------
    _type_: _description_
    """

    print("Loading RAW data (MoSAIC) ...", end=" ")
    with open(path, "rb") as f:
        data = f.read()

    data = np.fromstring(data, dtype=np.uint8)
    test = 0

    if test == 0:
        data = np.unpackbits(data)
        # data = unpack(data)
        # print(data[:10])
        print(np.shape(data))

        datsize = data.shape[0]
        data = data.reshape((int(datsize / 4), 4))
        # print(data[:10, :10])
        # print(np.shape(data))

        # Switch even rows and odd rows
        temp = copy.deepcopy(data[0::2])
        temp2 = copy.deepcopy(data[1::2])
        data[0::2] = temp2
        data[1::2] = temp

        # print(data[:10, :10])
        # print(np.shape(data))

        temp = np.concatenate(
            [
                data[0::3],
                np.array([0, 0, 0, 0] * 12000000, dtype=np.uint8).reshape(12000000, 4),
                data[2::3],
                data[1::3],
            ],
            axis=1,
        )

        # print(temp[:10, :20])
        # print(np.shape(temp))

        # Repack into image file
        udata = np.packbits(
            # udata = pack(
            # np.concatenate(
            #    [
            #        data[0::3],
            #        np.array([0, 0, 0, 0] * 12000000, dtype=np.uint8).reshape(12000000, 4),
            #        data[2::3],
            #        data[1::3],
            #    ],
            #    axis=1,
            temp
            # )
            .reshape(192000000, 1)
        ).tobytes()
        # print(udata[:10])
        # print(len(udata))

        img = np.fromstring(udata, np.dtype("u2"), (4000 * 3000)).reshape((3000, 4000))
        # print(img[:10, :10])
        # print(img.shape)
        y_size = 3000
        x_size = 4000
        image = np.zeros((y_size // 2, x_size // 2) + (3,), dtype=np.dtype("u2"))

        print(image.shape)
        image[:, :, 0] = img[1::2, 0::2]  # red channel
        image[:, :, 1] = (img[0::2, 0::2] + img[1::2, 1::2]) // 2  # green channel
        image[:, :, 2] = img[0::2, 1::2]  # blue channel

        print(image.shape)

    elif test == 1:
        data = np.unpackbits(data)
        datsize = data.shape[0]
        data = data.reshape((int(datsize / 4), 4))

        temp = []
        for i in range(16000000):
            temp.extend(
                [
                    data[i * 12 + 1],
                    [0, 0, 0, 0],
                    data[i * 12 + 3],
                    data[i * 12 + 0],
                    data[i * 12 + 2],
                    [0, 0, 0, 0],
                    data[i * 12 + 4],
                    data[i * 12 + 5],
                    data[i * 12 + 7],
                    [0, 0, 0, 0],
                    data[i * 12 + 9],
                    data[i * 12 + 6],
                    data[i * 12 + 8],
                    [0, 0, 0, 0],
                    data[i * 12 + 10],
                    data[i * 12 + 11],
                ]
            )

        udata = np.packbits(temp.reshape(192000000, 1)).tobytes()

        img = np.fromstring(udata, np.dtype("u2"), (4000 * 3000)).reshape((3000, 4000))

        y_size = 3000
        x_size = 4000
        image = np.zeros((y_size // 2, x_size // 2) + (3,), dtype=np.dtype("u2"))

        print(image.shape)
        image[:, :, 0] = img[1::2, 0::2]  # red channel
        image[:, :, 1] = (img[0::2, 0::2] + img[1::2, 1::2]) // 2  # green channel
        image[:, :, 2] = img[0::2, 1::2]  # blue channel

    elif test == 2:
        data = data.reshape(3000, 6000)[:, :]
        data = data.astype(np.uint16) << 2

        for byte in range(2):
            data[:, byte::3] |= (data[:, 2::3] >> ((2 - byte) * 2)) & 0b11
        data = np.delete(data, np.s_[2::3], 1)

        y_size = 3000
        x_size = 4000

        print(data.dtype)

        image = np.zeros((y_size // 2, x_size // 2) + (3,), dtype=data.dtype)

        image[:, :, 0] = data[1::2, 0::2]  # red channel
        # image[:, :, 1] = (data[0::2, 0::2] + data[1::2, 1::2]) // 2  # green channel
        # image[:, :, 2] = data[0::2, 1::2]  # blue channel
        image[:, :, 1] = data[1::2, 0::2]  # red channel
        image[:, :, 2] = data[1::2, 0::2]  # red channel

        print(image.shape)

    elif test == 3:
        y_size = 3000
        x_size = 4000

        image = np.zeros((y_size // 2, x_size // 2) + (3,), dtype=data.dtype)

        data = read_uint12(data).reshape(3000, 4000)
        # print(data.shape)
        image[:, :, 0] = data[1::2, 0::2]  # red channel
        image[:, :, 1] = (data[0::2, 0::2] + data[1::2, 1::2]) // 2  # green channel
        image[:, :, 2] = data[0::2, 1::2]  # blue channel

        # print(image.shape)

    print("Done!")
    return image[::2, ::2] / 65536


def read_uint12(data):
    # data = np.frombuffer(data_chunk, dtype=np.uint8)
    fst_uint8, mid_uint8, lst_uint8 = (
        np.reshape(data, (data.shape[0] // 3, 3)).astype(np.uint16).T
    )
    # fst_uint12 = (fst_uint8 << 4) + (mid_uint8 >> 4)
    # snd_uint12 = ((mid_uint8 % 16) << 8) + lst_uint8
    fst_uint12 = (fst_uint8 << 4) + (lst_uint8 >> 4)
    # print(fst_uint8)
    snd_uint12 = (mid_uint8 << 4) + (lst_uint8 << 4)
    return np.reshape(
        np.concatenate((fst_uint12[:, None], snd_uint12[:, None]), axis=1),
        2 * fst_uint12.shape[0],
    )
