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
import os
from pathlib import Path

from snowimagerpro.app.managers.jobs import threadpool
from snowimagerpro.app.managers.settings import user_config
from snowimagerpro.app.workers.run_func import ImageProcessor
from snowimagerpro.core.methods import helper

from ..base import LogicBase
from .model import model
from .viewr import Viewr, getSaveFileName, show_warning


def update_ui(func):
    def inner(self, *args):
        func(self, *args)
        model.signals.update_ui.emit()

    return inner


def check_db_integrity(fp):
    with open(fp) as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                _uid = int(row[0])
            except ValueError as e:
                print(e)
                show_warning(None, "Warning", f"Invalid database: {fp}")
                return False
    return True


class Logic(LogicBase):
    def __init__(self):
        super().__init__()

        self.viewr = Viewr

    @update_ui
    def add_h5_to_db(self, fp):
        if Path(fp).exists:
            uuid = helper.create_uuid()
            model.public.processed_images_db[uuid] = fp

            db = model.public.processed_image_dbs.items[model.public.processed_image_dbs.current_idx]
            db_fp = db.info["path"]

            with open(db_fp, "a") as f:
                print(f"Adding {fp} to {db_fp}")
                f.write(f"{uuid},{str(fp)}\n")

    @update_ui
    def add_db(self, fp):
        data_dir = user_config.get("analyzer.data_dir")
        if not os.path.exists(fp):
            return
        db_valid = check_db_integrity(fp)
        if not db_valid:
            return
        flag = model.public.processed_image_dbs.add_new_db(fp, data_dir)
        if flag:
            idx = model.public.processed_image_dbs.current_idx
            self.change_db(idx)
            model.public.widget_models["db_combo_2"].change_databases(idx)

    def remove_db(self, uuid):
        idx_removed = model.public.processed_image_dbs.remove_db(uuid)
        print("is_removed", idx_removed)
        if idx_removed:
            model.public.widget_models["db_combo_2"].removeRows(idx_removed, 1)
            if idx_removed == 0:
                new_uuid = model.public.processed_image_dbs.items[0].uuid
            elif idx_removed == len(model.public.processed_image_dbs.items):
                new_uuid = model.public.processed_image_dbs.items[idx_removed - 1].uuid
            else:
                print("not implemented")

            idx = model.public.processed_image_dbs.uuid_2_idx(new_uuid)
            model.public.widget_models["db_combo_2"].change_databases(idx)
            self.change_db(idx)

    @update_ui
    def change_db(self, index):
        image_db = {}
        dbs = model.public.processed_image_dbs.items
        if index is not None and dbs:
            db = model.public.processed_image_dbs.items[index]
            model.public.processed_image_dbs.current = db.uuid
            model.public.processed_image_dbs.current_idx = index

            _db_path = db.info["path"]
            if Path(_db_path).exists():
                db_valid = check_db_integrity(_db_path)
                if not db_valid:
                    return
                with open(_db_path) as f:
                    reader = csv.reader(f)
                    for row in reader:
                        _uid = int(row[0])
                        image_db[_uid] = row[1]

                print(image_db)
                # model.private["processed_image_db"] = image_db
                model.public.processed_images_db = image_db

    def change_data_dir(self, uuid, new_data_dir):
        print("Changing data dir to", new_data_dir)
        if uuid:
            model.public.processed_image_dbs.items[uuid].info["data_dir"] = new_data_dir
        else:
            print("No data dir changed")

    def load(self, fp):
        current_db = model.public.processed_image_dbs.current
        data_dir = model.public.processed_image_dbs.items[current_db].info["data_dir"]

        if not os.path.isabs(fp):
            fp = Path(data_dir) / fp
        else:
            fp = Path(fp)

        if fp.exists():

            def func():
                model.public.processed_img.load_from(fp)

            worker = ImageProcessor([func])
            worker.signals.result.connect(self.show_reflectance)
            threadpool.start(worker)

        else:
            show_warning(None, "Warning", f"File not found: {fp}")

    def calc_SSA(self):
        def func():
            model.public.processed_img.calculate_SSA()

        worker = ImageProcessor([func])
        worker.signals.result.connect(self.show_SSA)
        threadpool.start(worker)

    def calc_rho(self):
        def func():
            model.public.processed_img.calculate_rho()

        worker = ImageProcessor([func])
        worker.signals.result.connect(self.show_rho)
        threadpool.start(worker)

    def show_reflectance(self, img):
        img = model.public.processed_img

        if hasattr(img, "redcd_refl_img"):
            imgs = [img.total_refl_img, img.redcd_refl_img]
        else:
            imgs = [img.total_refl_img]

        self.show(imgs)

    def show_SSA(self, img):
        img = model.public.processed_img
        imgs = [
            {
                "SSA_profile": img.SSA_profile,
                "SSA_image": img.SSA_image,
            }
        ]

        self.show(imgs)

        for view in self.views:
            try:
                view.roi.sigRegionChangeFinished.connect(self.update_SSA)
                print("Connected")
            except AttributeError:
                pass

    def update_SSA(self, reg):
        print("Region changed", reg)
        model.public.processed_img.SSA_profile = [0, 0]

        for view in self.views:
            pass

    def show_rho(self):
        img = model.public.processed_img

        imgs = [
            {
                "SSA_profile": img.SSA_profile,
                "SSA_image": img.SSA_image,
                "density_profile": img.density_profile,
                "redcd_refl_img": img.redcd_refl_img,
            }
        ]

        self.show(imgs)

    def show(self, imgs):
        for img in imgs:
            view = self.viewr()
            view.show(img)
            view.closed.connect(self.remove_view)

            self.views = self.views + [view]

    def save_report(self):
        file = Path(model.public.processed_img.fp).stem
        path = user_config.get("report.path")

        fp = getSaveFileName(
            None, "Save Report", f"{path}/{file}_report", "Excel (*.xlsx)"
        )

        if fp:
            fp = Path(fp)
            if fp.suffix == "":
                fp = fp.with_suffix(".xlsx")
            elif fp.suffix == ".ods":
                fp = fp.with_suffix(".xlsx")
                show_warning(
                    None,
                    "Warning",
                    "Saving as .ods not supported yet. Open .xlsx and save as .ods, if necessary.",
                )

            model.public.processed_img.generate_report(fp)

            user_config.set("report.path", str(fp.parent))


logic = Logic()
