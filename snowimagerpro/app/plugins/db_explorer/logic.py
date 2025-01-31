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

import shutil
from pathlib import Path

from snowimagerpro.app.managers import user_config
from snowimagerpro.app.managers.data import raw_image_dbs
from snowimagerpro.app.managers.jobs import threadpool
from snowimagerpro.app.workers.run_func import ImageProcessor
from snowimagerpro.core.metadata import ImageMetadata
from snowimagerpro.core.methods import helper

from ..base import LogicBase, public_data
from .model import model
from .viewr import getSaveFileName, show_warning
import re


def focus_list(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        model.signals.focus_list.emit()

    return wrapper


def update_raw_image_dbs(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        model.public.raw_image_dbs._update.emit()
        model.public.img_set.regenerate_link_table()
        model.public.img_set.autosave_db()

    return wrapper


class Logic(LogicBase):
    def __init__(self):
        super().__init__()
        self.model = model

        model.signals.refresh_db.emit()

    def post_init(self):
        public_data.raw_image_dbs._update.connect(self.do_new_update)

    def do_new_update(self):
        print("RUNNING: do_new_update in db_explorer (logic)")

    def add_images_to_db(self, files_in, folders):
        files_out = []
        exts = [".BAY", ".dng"]

        if files_in is not None:
            files_in = sorted(files_in)

            for ext in exts:
                for file in files_in:
                    if file.endswith(ext.lower()):
                        files_out.append(file)

        if folders is not None:

            folders = sorted(folders)

            for folder in folders:
                for ext in exts:
                    for path in Path(folder).rglob(f"*{ext}", case_sensitive=False):
                        files_out.append(str(path))

            print("Found", len(files_out), "images with extension", ext)

        files_out = sorted(files_out)

        print("Adding images to db", files_out)

        curr_drk = -1
        curr_ref = 1

        for i, filepath in enumerate(files_out):
            uuid = helper.create_uuid()
            meta = ImageMetadata()

            meta.ID = uuid
            meta.filepath = filepath

            if i % 2 == 0:
                curr_drk += 1
            meta.drk_group = curr_drk

            if i % 2 == 0:
                if curr_ref == 1:
                    curr_ref = 0
                else:
                    curr_ref = 1
            meta.ref_group = curr_ref

            filename = Path(filepath).name
            wl = 0
            if "dark" in filename.lower():
                wl = 0
            elif match := re.search(r'\d{3}nm', filename):
                wl = int(match.group()[:-2])

            meta.wavelength = wl

            date_match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
            if date_match:
                meta.date = date_match.group()


            model.public.img_set._image_db[uuid] = meta

        print(len(model.public.img_set._image_db), "images in current image db")

        # model.signals.refresh_db.emit()
        model.public.widget_models["image_list"].refresh()
        model.public.widget_models["image_tree"].refresh()

        self.write_to_db()

    def remove_images_from_db(self, uuids):
        print("Removing images with uuids", uuids)
        print(model.public.img_set._image_db.keys())
        for uuid in uuids:
            model.public.img_set._image_db.pop(int(uuid))

        model.public.widget_models["image_list"].refresh()
        model.public.widget_models["image_tree"].refresh()

    def backup_db(self, fp):
        # TODO: handle multiple backups
        if not isinstance(fp, Path):
            fp = Path(fp)
        fp_bak = fp.with_suffix(fp.suffix + ".bak")
        shutil.copy(fp, fp_bak)

    def write_to_db(self, fp=None):
        model.public.img_set.save_db(fp)

        if not fp:  # if no file path is given, write to current db after backing up
            fp = model.public.img_set.current_db_path
            self.backup_db(fp)

        # TODO: Check if database has actually changed (see settings.manager)

    def write_to_new_db(self, fp):
        db = model.public.img_set
        fp = getSaveFileName(
            None, "Save database as", str(db.current_db_path), "Database (*.csv)"
        )
        self.write_to_db(fp)

    def copy_metadata(self, selected_settings):
        self.clipboard = {}

        uuid = model.private["current_img_uuid"]
        print("Copying metadata for image with uuid", uuid)
        _meta = model.public.img_set._image_db[int(uuid)]

        for key in selected_settings:
            print("Copying metadata for key", key)
            self.clipboard[key] = getattr(_meta, key)

    @update_raw_image_dbs
    def paste_metadata(self, uuids):
        for uuid in uuids:
            self.paste_metadata_single(uuid)

    def paste_metadata_single(self, uuid):
        _meta = model.public.img_set._image_db[int(uuid)]

        for key in self.clipboard:
            print("Pasting metadata for key", key)
            print(self.clipboard[key])
            _meta[key] = self.clipboard[key]

    def add_db(self, fp):
        flag = raw_image_dbs.add_new_db(fp)
        if flag:
            self.update.emit(self)

    def remove_db(self, uuid, delete_from_disk=False):
        idx_removed = raw_image_dbs.remove_db(uuid, delete_from_disk)
        print("is_removed", idx_removed)
        if idx_removed:
            model.public.widget_models["db_combo"].removeRows(idx_removed, 1)
            if idx_removed == 0:
                new_uuid = raw_image_dbs.items[0].uuid
            elif idx_removed == len(raw_image_dbs.items):
                new_uuid = raw_image_dbs.items[-1].uuid
            else:
                print("no way")
            self.select_db(new_uuid)

    def delete_db(self, uuid):
        self.remove_db(uuid, delete_from_disk=True)

    def select_db(self, uuid):
        print(f"Selecting db with uuid {uuid}")
        raw_image_dbs.current = uuid
        raw_image_dbs.current_idx = raw_image_dbs.uuid_2_idx(uuid)
        user_config.set("raw_image_dbs_last", raw_image_dbs.current_idx)
        user_config.save()
        raw_image_dbs.select_db(uuid)
        self.update.emit(self)

    def change_data_dir(self, uuid, new_data_dir):
        print("Changing data dir to", new_data_dir)
        # uuid = model.public.databases.current
        if uuid:
            model.public.raw_image_dbs.items[uuid].info["data_dir"] = new_data_dir
        else:
            print("No data dir changed")
        model.public.img_set._data_dir = new_data_dir

    def load_single_image(self, uuid):
        print("db explorer load image with uuid", uuid)
        model.private["current_img_uuid"] = uuid
        model.private["current_db_entry"] = public_data.img_set._image_db[int(uuid)]
        model.private["current_data_dir"] = public_data.img_set._data_dir

        print("data dir is ", model.public.img_set._data_dir)

        fp = Path(model.private["current_data_dir"]) / Path(
            model.private["current_db_entry"].filepath
        )
        print(fp)

        if fp.exists():

            def func():
                model.private["current_img"].load_from(
                    model.private["current_db_entry"],
                    _dir=model.private["current_data_dir"],
                )

            worker = ImageProcessor([func])

            worker.signals.result.connect(self.do_update)

            threadpool.start(worker)

        else:
            show_warning(None, "Warning", f"File not found: {fp}")

    def do_update(self):
        model.signals.update_dbs.emit()
        model.signals.change_img.emit()
        # model.signals.refresh_db.emit()

    @focus_list
    @update_raw_image_dbs
    def update_img_type(self, val, uuids):
        for uuid in uuids:
            model.public.img_set._image_db[int(uuid)].img_type = str(val)

    @focus_list
    @update_raw_image_dbs
    def update_current_drk_group(self, val, uuids):
        for uuid in uuids:
            model.public.img_set._image_db[int(uuid)].drk_group = int(val)

    @focus_list
    @update_raw_image_dbs
    def update_current_ref_group(self, val, uuids):
        for uuid in uuids:
            model.public.img_set._image_db[int(uuid)].ref_group = int(val)

    @focus_list
    @update_raw_image_dbs
    def update_current_meas_group(self, val, uuids):
        for uuid in uuids:
            model.public.img_set._image_db[int(uuid)].meas_group = str(val)

    @focus_list
    @update_raw_image_dbs
    def update_coords_mm(self, val, uuids):
        for uuid in uuids:
            model.public.img_set._image_db[int(uuid)].coords_mm = str(val)

    @focus_list
    @update_raw_image_dbs
    def update_px2mm(self, val, uuids):
        for uuid in uuids:
            model.public.img_set._image_db[int(uuid)].px_2_mm = float(val)

    @focus_list
    @update_raw_image_dbs
    def update_wavelength(self, val, uuids):
        for uuid in uuids:
            model.public.img_set._image_db[int(uuid)].wavelength = float(val)

    # @update_raw_image_dbs
    def update_ROI(self, idx, _roi):
        print("Updating ROI for idx", idx)
        uuid = model.private["current_img_uuid"]
        model.public.img_set._image_db[int(uuid)].ROI[idx[0]][idx[1]] = _roi

    # @update_raw_image_dbs
    def update_coords_pix(self, _coords_pix):
        uuid = model.private["current_img_uuid"]
        model.public.img_set._image_db[int(uuid)].coords_pix = str(_coords_pix)

    # @focus_list
    @update_raw_image_dbs
    def add_ROI(self, uuids, which="white"):
        print(f"Adding {which} ROI")

        db = model.public.img_set

        for uuid in uuids:
            _ROI = db._image_db[int(uuid)].ROI

            if which == "gray":
                new_ROI = [[0.5, 0.5], [0.6, 0.6]]
                _ROI[0].append(new_ROI)
            elif which == "white":
                new_ROI = [[0.3, 0.3], [0.4, 0.4]]
                _ROI[1].append(new_ROI)

            db._image_db[uuid].update({"ROI": _ROI})

        # model.signals.redraw_img.emit()

    # @focus_list
    @update_raw_image_dbs
    def remove_ROI(self, uuids, which="white"):
        print(f"Removing {which} ROI")

        db = model.public.img_set

        for uuid in uuids:
            _ROI = db._image_db[uuid].ROI

            if which == "gray":
                _ROI[0].pop()
            elif which == "white":
                _ROI[1].pop()

            db._image_db[uuid].update({"ROI": _ROI})

        # model.signals.redraw_img.emit()


logic = Logic()
