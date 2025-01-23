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

from snowimagerpro.app.managers import user_config
from snowimagerpro.app.managers.jobs import threadpool
from snowimagerpro.app.workers.run_func import ImageProcessor

from ..base import LogicBase, public_data
from .viewr import AddToDatabaseDialog, Viewr

logger = "image_processor.logic"


class Logic(LogicBase):
    def __init__(self):
        super().__init__()

    def load(self):
        logging.getLogger(logger).info(f"Loading uuid(s): {public_data.uuids_selected}")

        uuids = [int(uuid) for uuid in public_data.uuids_selected]

        def func():
            public_data.img_set.load_images(uuids)

        worker = ImageProcessor([func])
        worker.signals.result.connect(self.update_view)
        threadpool.start(worker)

    def ffc(self):
        def func():
            public_data.img_set.ffc()

        worker = ImageProcessor([func])
        worker.signals.result.connect(self.result_ffc)
        threadpool.start(worker)

    def result_ffc(self, result):
        print(result)

    def remove_ffc(self):
        if hasattr(public_data.img_set, "imgs_post_ffc"):
            del public_data.img_set.imgs_post_ffc
        else:
            print("No FFC images to remove.")

    def refl_cal(self):
        def func():
            public_data.img_set.refl_cal()

        worker = ImageProcessor([func])
        threadpool.start(worker)

    def remove_refl(self):
        if hasattr(public_data.img_set, "imgs_post_refl_cal"):
            del public_data.img_set.imgs_post_refl_cal
        else:
            print("No refl_cal images to remove.")

    def undistort_images(self):
        path = "/home/lrrr/Documents/SLF_local/apps/SnowImagerPro/snowimagerpro/core/calibration/distortion_calib_06.json"

        def func():
            public_data.img_set.undistort(path)

        worker = ImageProcessor([func])
        threadpool.start(worker)

    def remove_undistort(self):
        if hasattr(public_data.img_set, "imgs_post_undistort"):
            del public_data.img_set.imgs_post_undistort
        else:
            print("No undistorted images to remove.")

    def update_overlap_x(self, value):
        public_data.img_set.overlap_x = value
        user_config.set("processor.overlap_x", value)

    def update_overlap_y(self, value):
        public_data.img_set.overlap_y = value
        user_config.set("processor.overlap_y", value)

    def stitch_images(self):
        def func():
            public_data.img_set.stitching()

        worker = ImageProcessor([func])

        worker.signals.result.connect(self.show_stitched)

        threadpool.start(worker)

    def show_raw(self, uuid=None, show_dark=True, show_ref=True):
        if uuid:
            imgs = {uuid: public_data.img_set._selected_images[uuid]}
            show_dark = True
            show_ref = True
        else:
            imgs = public_data.img_set._selected_images

        if not show_dark:
            try:  # TODO: Remove this when sorting out metadata issue in snowpy
                imgs = {
                    key: val for key, val in imgs.items() if val._meta.wavelength != 0
                }
            except Exception as e:
                imgs = {
                    key: val
                    for key, val in imgs.items()
                    if val._meta["wavelength"] != 0
                }

        if not show_ref:
            try:
                imgs = {
                    key: val for key, val in imgs.items() if val._meta.img_type != "ref"
                }
            except Exception as e:
                imgs = {
                    key: val
                    for key, val in imgs.items()
                    if val._meta["img_type"] != "ref"
                }

        self._view(imgs)

    def show_processed(self):
        img_set = public_data.img_set

        if hasattr(img_set, "imgs_post_undistort"):
            imgs = img_set.imgs_post_undistort
        elif hasattr(img_set, "imgs_post_refl_cal"):
            imgs = img_set.imgs_post_refl_cal
        elif hasattr(img_set, "imgs_post_ffc"):
            imgs = img_set.imgs_post_ffc
        else:
            print("No processed images to show.")
            return
        # imgs = public_data.img_set._tmp
        self._view(imgs)

    def show_stitched(self):
        imgs = public_data.img_set.stitched_image
        self._view(imgs, origin="lower")

    def _view(self, imgs, origin="upper"):
        N = 0
        for uuid, img in imgs.items():
            N += 1

            view = Viewr(img, origin=origin)
            view.closed.connect(self.remove_view)

            self.views = self.views + [view]

            logging.getLogger(logger).info(
                f"Opened image viewer for image with uuid {uuid}"
            )

        logging.getLogger(logger).info(f"Opened {N} image viewer(s)")

    def save(self, folder=None):
        if folder:
            user_config.set("processor.h5_path", folder)

        def func(folder=folder):
            return public_data.img_set.save_as_h5(folder=folder)

        worker = ImageProcessor([func])

        dlg = AddToDatabaseDialog()

        worker.signals.result.connect(dlg.add_fp)
        threadpool.start(worker)

        dlg.exec()

    def close_views(self):
        return super().close_views()


logic = Logic()
