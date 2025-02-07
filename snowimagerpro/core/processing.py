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

import concurrent.futures
import json
import yaml
import logging
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Union
import exifread

import cv2 as cv
import discorpy.post.postprocessing as post
import h5py
import numpy as np
from scipy import ndimage

import snowimagerpro.core.methods.processing as pro
from snowimagerpro.core.metadata import ImageMetadata, StitchedMetadata
from snowimagerpro.core.methods import helper
from snowimagerpro.core.validators import OutputDataValidator

DEBUG = 0

logger = "core.processing"


class ImageSet:
    def __init__(self):
        self.total_progress = 0
        self.status_msg = ""

        self.autosave_on = False

        self.current_db_path = None

        self._db_path = ""
        self._data_dir = ""

        self.overlap_x = 200
        self.overlap_y = 200

    def inc_progress_by(self, value, status_msg=None, reset=False):
        """
        Increment the progress by a specified value.

        **PATCHED/DECORATED IN APP TO UPDATE GUI PROGRESS BAR**

        If the total progress exceeds or equals 100 after the increment,
        the total progress is reset to 0. Otherwise, the specified value
        is added to the total progress.

        Args:
            value (int): The value to increment the progress by.
        """

        if reset:
            self.total_progress = 0
        else:
            if self.total_progress + value >= 100:
                self.total_progress = 100
            else:
                self.total_progress += value

        if status_msg:
            self.status_msg = status_msg

        if self.total_progress >= 99:
            self.total_progress = 100
            self.status_msg = self.status_msg + " Done!"

    def reset(self):
        if hasattr(self, "imgs_post_ffc"):
            del self.imgs_post_ffc
        if hasattr(self, "imgs_post_refl_cal"):
            del self.imgs_post_refl_cal
        if hasattr(self, "imgs_post_undistort"):
            del self.imgs_post_undistort
        if hasattr(self, "stitched_image"):
            del self.stitched_image

    def load(self):
        self.inc_progress_by(11, status_msg="")
        print("loading image set")
        self.load_db("path/to/db")

    def load_db(self, db_path: str | Path, data_dir: str | Path | None = None):
        self.current_db_path = db_path

        if data_dir:
            self._data_dir = data_dir

        image_db = pro.load_db(db_path)

        image_db = helper.expand_db_by_meas_group(image_db)

        for entry in image_db.values():
            if data_dir:
                fp = str(data_dir / Path(entry.filepath))
            else:
                fp = entry.filepath

            if Path(fp).exists():

                meta_path = fp.split("-")[:-1]
                meta_path = "-".join(meta_path) + "_metadata.yaml"

                with open(meta_path, "r") as f:
                    meta = yaml.safe_load(f)
                entry.meta = meta

                with open(fp, "rb") as f:
                    exif = exifread.process_file(f)
                entry.exif = exif



        self._image_db = image_db

        self.generate_link_table()

    def autosave_db(self):
        if self.autosave_on:
            self.save_db()

    def save_db(self, fp=None):
        if not fp:
            fp = self.current_db_path

        with open(str(fp), "w") as f:
            f.write(",".join(ImageMetadata.to_key_list()) + "\n")

            for entry in self._image_db.values():
                _tmp = []
                for _key, item in zip(entry.to_key_list(), entry.to_list()):
                    if _key in ["_exif", "exif"]:
                        continue
                    if isinstance(item, list):
                        _tmp.append('"' + str(item) + '"')
                    else:
                        if _key in [
                            "meas_group",
                            "aux_data",
                        ]:  # FIX because of commas in csv
                            _tmp.append('"' + str(item) + '"')
                        else:
                            _tmp.append(str(item))

                f.write(",".join(_tmp) + "\n")

    def regenerate_link_table(self):
        self.generate_link_table()

    def generate_link_table(self):
        link_table = {}
        db_path = self.current_db_path
        image_db = self._image_db

        logging.getLogger(logger).info(f"Generating link table for {db_path}")

        has_ref = False
        for key in image_db.keys():
            if image_db[key].img_type == "ref":
                has_ref = True
                break

        if has_ref:
            for key, entry in image_db.items():
                if entry.wavelength != 0:
                    link_entry = {}
                    link_entry.update(
                        {
                            "dark_id": v.ID
                            for k, v in image_db.items()
                            if v.drk_group == entry.drk_group
                            and v.meas_group == entry.meas_group
                            and v.wavelength == 0
                            and k != key
                        }
                    )

                try:
                    if entry.img_type not in ["ref"]:
                        link_entry.update(
                            {
                                "ref_id": v.ID
                                for k, v in image_db.items()
                                if v.ref_group == entry.ref_group
                                and v.meas_group == entry.meas_group
                                and v.wavelength != 0
                                and v.img_type == "ref"
                            }
                        )

                    link_table.update({key: deepcopy(link_entry)})
                except Exception as e:
                    print("Error linking images.")

        if not link_table:
            print("No reference images found.")

        self._link_table = link_table

    def load_images(self, list_of_idx):
        self.reset()

        self._selected_images = {}
        futures = list()
        self.inc_progress_by(1, status_msg="Loading images ...", reset=True)
        N = len(list_of_idx)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for meta in [self._image_db[i] for i in list_of_idx]:
                img = Image()
                future = executor.submit(
                    img.load_from, meta, self._data_dir
                )  # running in parallel to speed up loading
                future.add_done_callback(
                    lambda event, progress=(100 / N): self.inc_progress_by(progress)
                )

                futures.append(future)
                self._selected_images[meta.ID] = img

        for future in futures:
            future.result()  # catch exceptions

    def ffc(self):
        _images_in = self._selected_images
        _images_out = {}
        futures = list()
        self.inc_progress_by(1, status_msg="Flat-field correction ...", reset=True)

        N = sum(
            1
            for img in _images_in.values()
            if img._meta.img_type not in ["ref"] and img._meta.wavelength != 0
        )

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for key in _images_in.keys():
                link = self._link_table[key]

                if "ref_id" not in link:
                    # skip reference images
                    continue

                img = deepcopy(_images_in[key])

                if img._meta.wavelength == 0:
                    # skip dark images
                    continue

                dark = _images_in[link["dark_id"]]
                try:
                    ref = _images_in[link["ref_id"]]
                except KeyError:
                    return ReferenceError
                # ref._data = ref._data.astype(np.float32) # TODO: Smooth ref and ref_dark
                # ref._data = cv.bilateralFilter(ref._data, 15, 75, 75)

                ref_dark_id = self._link_table[link["ref_id"]]["dark_id"]
                ref_dark = _images_in[ref_dark_id]
                # ref_dark._data = ref_dark._data.astype(np.float32)
                # ref_dark._data = cv.bilateralFilter(ref_dark._data, 15, 75, 75)

                # ffc: (img - dark) / (ref - ref_dark) * m
                future = executor.submit(img.do_ffc, dark, ref, ref_dark)
                future.add_done_callback(
                    lambda event, progress=(100 / N): self.inc_progress_by(progress)
                )
                futures.append(future)

                _images_out[key] = img

        for future in futures:
            future.result()

        self.imgs_post_ffc = _images_out

    def refl_cal(self):
        _images_in = deepcopy(self.imgs_post_ffc)
        _images_out = {}
        print("performing reflectance calibration")
        futures = list()
        self.inc_progress_by(1, status_msg="Calibrating reflectance ...", reset=True)
        N = len(_images_in)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for key, img in _images_in.items():
                # refl_cal: m * img + b
                future = executor.submit(img.do_refl_cal)
                future.add_done_callback(
                    lambda event, progress=(100 / N): self.inc_progress_by(progress)
                )
                futures.append(future)

                _images_out[key] = img

        for future in futures:
            future.result()

        self.imgs_post_refl_cal = _images_out

    def undistort(self, path):
        if hasattr(self, "imgs_post_refl_cal"):
            _images_in = deepcopy(self.imgs_post_refl_cal)
        elif hasattr(self, "imgs_post_ffc"):
            _images_in = deepcopy(self.imgs_post_ffc)
        else:
            print("No images to undistort.")
            return

        _images_out = {}
        futures = list()
        self.inc_progress_by(1, status_msg="Removing image distortion ...", reset=True)
        N = len(_images_in)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for key, img in _images_in.items():
                # img = deepcopy(self._tmp[key])

                future = executor.submit(lambda path=path: img.do_undistort(path))
                future.add_done_callback(
                    lambda event, progress=(100 / N): self.inc_progress_by(progress)
                )
                futures.append(future)

                _images_out[key] = img

        for future in futures:
            future.result()

        self.imgs_post_undistort = _images_out

    def stitching(self):
        if hasattr(self, "imgs_post_undistort"):
            imgs = self.imgs_post_undistort
        elif hasattr(self, "imgs_post_refl_cal"):
            imgs = self.imgs_post_refl_cal
        elif hasattr(self, "imgs_post_ffc"):
            imgs = self.imgs_post_ffc
        else:
            print("No images to stitch.")
            return

        sorted_images = pro.image_sorting(imgs)  #

        for _group in sorted_images.values():
            _group = pro.coords_mm_to_pix(_group)
            for image in _group.values():
                print("here")
                print(image._pos)

        self.stitched_image = {}

        futures = {}
        self.inc_progress_by(1, status_msg="Stitching images ...", reset=True)
        N = len([val for val in sorted_images.values() if len(val.values()) > 0])
        print(f"sorted images are {sorted_images}")
        i = 0
        # TODO: pair-wise processing?
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _img_type, _group in sorted_images.items():
                if len(_group.values()) < 1:
                    continue
                future = executor.submit(
                    pro.image_blending,
                    _group,
                    algo="laplPyr",
                    sigmaX=self.overlap_x,
                    sigmaY=self.overlap_y,
                )
                future.add_done_callback(
                    lambda event, progress=(100 / N): self.inc_progress_by(progress)
                )

                futures[(i, _img_type)] = future
                i += 1

        for __tmp, future in futures.items():
            _grp, _img_type = __tmp
            image, meta, exif = future.result()

            wavelengths = set()
            px2mms = set()
            dates = set()
            locations = set()

            for _meta in meta:
                # key = _meta[0]
                _meta[1]["filepath"] = str(_meta[1]["filepath"])
                wavelengths.add(_meta[1]["wavelength"])
                px2mms.add(_meta[1]["px_2_mm"])
                if _meta[1]["img_type"] != "ref":
                    dates.add(_meta[1]["date"])
                locations.add(_meta[1]["location"])

            if len(wavelengths) > 1:
                print("Error: multiple wavelengths in stitched image.")
            else:
                wavelength = next(iter(wavelengths))

            if len(px2mms) > 1:
                print("Error: multiple px2mm in stitched image.")
            else:
                px2mm = next(iter(px2mms))

            if len(dates) > 1:
                print("Error: multiple dates in stitched image.")
            else:
                date = next(iter(dates))

            if len(locations) > 1:
                print("Error: multiple locations in stitched image.")
            else:
                location = next(iter(locations))


            stitched_image = Image()
            stitched_image._data = image
            stitched_image._meta = StitchedMetadata
            stitched_image._meta["img_type"] = _img_type
            stitched_image._meta["px_2_mm"] = px2mm
            stitched_image._meta["wavelength"] = wavelength
            stitched_image._meta["date"] = date
            stitched_image._meta["location"] = location

            stitched_image._meta["orig_meta"] = deepcopy(meta)

            stitched_image._exif = exif

            self.stitched_image[_img_type] = deepcopy(stitched_image)
            del stitched_image

        # TODO: add group [_img_type][_grp] for optional col-major or row-major blending
        # TODO: If col/row-major blending perform here

    def save_as_h5(self, fp=None, folder=None):
        for key, img in self.stitched_image.items():
            print(f"Saving image {key} to h5.")
            fn = img.save_as(fp, folder)

        return fn


class Image:
    def __init__(self) -> None:
        self._uid: int
        self._data: Union[np.ndarray, None]
        self._meta: Union[ImageMetadata, dict]
        self._exif = None

    def load_from(self, _from, _dir=None, preview=False):
        if isinstance(_from, Path):
            fp = _from
        elif isinstance(_from, str):
            fp = Path(_from)
        elif isinstance(_from, ImageMetadata):
            fp = _from.filepath
            self._meta = _from
        else:
            print("invalid input of type " + str(type(_from)))

        if _dir:
            if isinstance(_dir, str):
                _dir = Path(_dir)
            fp = _dir / fp

        logging.getLogger(logger).info(f"Loading image {fp}")

        if preview:
            self._data, self._exif = pro.load_preview(fp)
        else:
            self._data, self._exif = pro.load_image(fp)

    def do_ffc(self, dark, ref, ref_dark):
        img = self._data
        dark = dark._data
        ref = ref._data
        ref_dark = ref_dark._data

        _img = img - dark
        _ref = ref - ref_dark
        _ref[_ref == 0] = 1e-10
        _img = _img / _ref * 0.5

        _img[_img > 1.25] = 1.25
        _img[_img < -0.25] = -0.25

        self._data = _img

    def do_refl_cal(self):
        img = self._data
        meta = self._meta

        # per target and per channel average in ROI
        avs_gray = pro.average_in_ROI(img, meta.ROI[0])
        avs_white = pro.average_in_ROI(img, meta.ROI[1])

        # TODO: auto-check average values and raise error if the channels are not the same
        # TODO: Average if they are

        # per channel mean of averages (i.e. averaging targets)
        mean_gray = np.nanmean(avs_gray, axis=0)
        mean_white = np.nanmean(avs_white, axis=0)

        logging.info(
            f"image {meta.ID} with wavelength {meta.wavelength} has avs_gray: {mean_gray} and avs_white: {mean_white}"
        )

        m1 = (0.94 - 0.498) / (mean_white - mean_gray)
        m2 = (0.94 - 0.000) / (mean_white - 0)
        m3 = (0.498 - 0.00) / (mean_gray - 0)

        m = (3 * m1 + m2 + m3) / 5  # bias towards m1

        b1 = 0.94 - (m * mean_white)
        b2 = 0.498 - (m * mean_gray)

        b = (b1 + b2) / 2

        img = m * img + b

        # img with 3 channels, however, channel values should be equal
        # keep 3 channels to double check post-processing
        self._data = img

    def do_undistort(self, path):
        img = self._data
        meta = self._meta

        sn = pro.get_sn(self._exif)
        logging.info(f"undistorting image {meta.ID} with camera serial number {sn}.")
        print(f"undistorting image {meta.ID} with camera serial number {sn}.")

        _sn = "".join(filter(str.isdigit, sn))
        path = f"snowimagerpro/core/calibration/distortion_calib_{_sn}.json"
        print(f"using calibration data from {path}")

        try:
            with open(path) as f:
                calibration = json.load(f)
        except IOError as e:
            raise e

        logging.info(f"Calibration for serial number {calibration['Serial No.']}")
        print(f"Calibration for serial number {calibration['Serial No.']}")

        if sn == calibration["Serial No."]:
            if "top" in str(meta.filepath).lower():
                key = "top"
            else:
                key = "bottom"

            xcenter = calibration[key]["xcenter"]
            ycenter = calibration[key]["ycenter"]
            factors = calibration[key]["factors"]
            rot = calibration[key]["rotation"]
            shift = calibration[key]["shift"]
            stretch = calibration[key]["stretch"]

            print(key)
            print(xcenter)
            print(ycenter)
            print(factors)
            print(rot)
            print(stretch)

            # TODO: Need to account for image binning! parameters
            # (at least xcenter and ycenter) are in pixel coordinates
            # what about the factors ?

            if len(img.shape) == 3:
                print("image is 3d")
                _tmp = np.zeros_like(img)
                for i in range(3):
                    _tmp[:, :, i] = post.unwarp_image_backward(
                        img[:, :, i], xcenter, ycenter, np.array(factors)
                    )
            else:
                print("image is 2d")
                _tmp = post.unwarp_image_backward(
                    img, xcenter, ycenter, np.array(factors)
                )

            print(f"rotating image by {rot} degrees.")
            _tmp = ndimage.rotate(_tmp, angle=rot, reshape=False, mode="nearest")

            if stretch != 1:
                print(key)
                print(stretch)
                stretch_factor = 0.995
                img_size = None
                _tmp = cv.resize(
                    _tmp,
                    img_size,
                    fx=stretch_factor,
                    fy=stretch_factor,
                    interpolation=cv.INTER_LINEAR,
                )
                print("stretching image by factor", stretch_factor)
                print("new image size is", _tmp.shape)
                __tmp = np.zeros_like(img)
                print(_tmp.shape)
                print(__tmp.shape)
                if _tmp.shape[0] > __tmp.shape[0]:
                    __tmp = _tmp[: __tmp.shape[0], : __tmp.shape[1]]
                elif _tmp.shape[0] < __tmp.shape[0]:
                    __tmp[: _tmp.shape[0], : _tmp.shape[1]] = _tmp[:, :]
                else:
                    __tmp = _tmp

                _tmp = __tmp

            if shift != 0:
                print("shifting image by", shift, "pixels.")
                _tmp = np.roll(_tmp, shift, axis=1)
            # TODO: possible alternative to avoid scipy.ndimage.rotate
            # (h, w) = _tmp.shape[:2]
            # (cX, cY) = (w // 2, h // 2)
            # mat = cv.getRotationMatrix2D((cX, cY), rot, 1)
            # _tmp = cv.warpAffine(_tmp, mat, (w, h))

            self._data = _tmp

        else:
            logging.warning("Serial number does not match calibration data.")

    def save_as(self, fp=None, folder=None, filetype="h5"):
        if filetype.lower() in ["h5", "hdf5"]:
            exif = self._exif[-1][1]
            orig_meta = self._meta["orig_meta"][-1][1]

            # img_type = orig_meta["img_type"]
            img_type = self._meta["img_type"]
            date = orig_meta["date"]
            location = orig_meta["location"]

            if fp is not None:
                fn = fp
            else:
                dtime = datetime.now().strftime("%Y%m%d_%H%M")
                fn = f"{date}_{location}/processedOn_{dtime}.h5"

            #if not folder:
            #    output_file = Path("tests/data/test_out/" + fn)
            #else:
            #if isinstance(folder, str):
            #    output_file = Path(folder) / Path(fn)
            #else:
            #    output_file = folder / Path(fn)

            output_file = Path(fn)

            output_file.parent.mkdir(exist_ok=True, parents=True)

            if DEBUG:
                output_file = output_file.with_suffix(".DEBUG.h5")

            logging.info(f"saving to: {output_file}")

            image = self._data * 1023
            image[image < 0] = 0
            image[image > 1023] = 1023
            image = image.astype(np.uint16)

            # TODO: maybe, double check against schema
            data = {
                "image": image.tolist(),
                "pix2mm": orig_meta["px_2_mm"],
                "reference_pix_xz": self._meta["coords_pix"],
                "reference_pos_xz": self._meta["coords_mm"],
            }

            print(self._meta)
            # print(data)
            try:
                OutputDataValidator(data)
                logging.info("Validation successful.")
            except Exception as e:
                logging.warning(f"Validation failed: {e}")
                return

            _data = {
                "image": {
                    "data": image.tolist(),
                    "attrs": {
                        "pix2mm": orig_meta["px_2_mm"],
                        "reference_pix_xz": self._meta["coords_pix"],
                        "reference_pos_xz": self._meta["coords_mm"],
                    },
                }
            }

            sn = pro.get_sn(exif)

            logging.info(f"serial number is {sn}.")

            if sn in ["snowimager-01"]:
                aux_data = {
                    "timestamp": exif["metadata"]["timestamp"],
                    "timezone": exif["metadata"]["timezone"],
                    "longitude": "",
                    "latitude": "",
                    "software_version": exif["metadata"]["software_version"],
                    "wavelength": exif["metadata"]["wavelength"],
                    "board_temperature_electronics_side": "",
                    "board_temperature_led_side": "",
                }
            elif sn in ["snowimager-06", "snowimager-07"]:
                aux_data = {
                    "timestamp": str(exif["Image DateTimeOriginal"]),
                    "timezone": "UTC",
                    "longitude": exif["metadata"]["longitude"],
                    "latitude": exif["metadata"]["latitude"],
                    "software_version": exif["metadata"]["software_version"],
                    "wavelength": exif["metadata"]["wavelength"],
                    "board_temperature_electronics_side": exif["metadata"][
                        "temperatures"
                    ]["board_temperature_electronics_side"],
                    "board_temperature_led_side": exif["metadata"]["temperatures"][
                        "board_temperature_led_side"
                    ],
                }

            with h5py.File(output_file, "a") as f:
                images_grp = f.require_group("SnowImage(s)")

                for key, entry in aux_data.items():
                    images_grp.attrs[key] = entry

                # try:
                #    image_grp = images_grp.create_group(img_type)
                #    for key in data.keys():
                #        if key == "image":
                #            _test = image_grp.create_dataset(
                #                key,
                #                data=data[key],
                #                compression="gzip",
                #                shuffle=True,
                #                dtype=np.int16,
                #            )
                #            _test.attrs["bla"] = 0
                #        else:
                #            image_grp.create_dataset(key, data=data[key])

                # except Exception as e:
                #    print("Error while saving to hdf5 file.")
                #    print(e)
                print("image type is ", img_type)
                try:
                    image_grp = images_grp.create_group(img_type)
                    dataset = image_grp.create_dataset(
                        "image",
                        data=_data["image"]["data"],
                        compression="gzip",
                        shuffle=True,
                        dtype=np.int16,
                    )
                    for attr in _data["image"]["attrs"]:
                        val = _data["image"]["attrs"][attr]

                        dataset.attrs[attr] = val

                except Exception as e:
                    print("Error while saving to hdf5 file.")
                    print(e)

        else:
            logging.warning(f"Unsupported filetype {filetype}")

        return output_file
