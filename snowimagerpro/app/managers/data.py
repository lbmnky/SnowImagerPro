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

import os
import logging
from send2trash import send2trash
from typing import Any, Union, overload

from snowimagerpro.app._core import Image, ImageSet, ImageForAnalysis
from snowimagerpro.core.methods import helper
from .settings import user_config

from snowimagerpro.app.popups import show_warning

from ._utils import BetterDict
from collections import namedtuple

logger = "managers.data"

def save_user_config(func):
    def wrapper(*args, **kwargs):
        flag = func(*args, **kwargs)
        logging.getLogger(logger).info(f"Saving user config: {flag}")
        if flag:
            user_config.save()
        return flag

    return wrapper


WidgetInstance = namedtuple("WidgetInstance", ["widget", "origin"])


class PublicDataModel:
    def __init__(self, widget_models: dict = {}) -> None:
        ## Single image only
        self.single_img = Image()

        ## Image set used in image processor and modified in db explorer
        self.raw_image_dbs = raw_image_dbs
        self.img_set = ImageSet()
        self.img_set._image_db = {}  # FIX: Needed to load without ANY db in settings file
        self.sortby = "date"
        self.uuids_selected: list[str] = []

        ## Processed reflectance image for post-processing (SSA and density calculation)
        self.processed_image_dbs = processed_image_dbs
        self.processed_images_db: dict[str, str] = {} ## NO NEED FOR PUBLIC ACCESS
        self.processed_img = ImageForAnalysis()

        self.widget_models: dict = {}
        for name, Model in widget_models.items():
            self.add_widget_model(name, Model)

    def add_widget_model(self, name, Model):
        # HINT: Need to modify in order to use same ui elements for different data models
        if name == "db_combo":
            self.widget_models[name] = Model(self.raw_image_dbs)
        elif name == "db_combo_2":
            self.widget_models[name] = Model(self.processed_image_dbs)
        elif name == "image_list":
            self.widget_models[name] = Model(self.img_set)
        else:
            self.widget_models[name] = Model(self)

    def initialize(self) -> None:
        ## raw_image database
        self.raw_image_dbs.initialize(user_config.get("raw_image_dbs"))

        if self.raw_image_dbs:
            uuid = self.raw_image_dbs.current
            self.raw_image_dbs.current = uuid  # TODO: Why double?


            ## Load raw_image database
            #info = self.raw_image_dbs.items[uuid].info  # >> this yields info
            #self.img_set.load_db(info["path"], data_dir=info["data_dir"])

        ## processed_image database
        self.processed_image_dbs.initialize(user_config.get("processed_image_dbs"))

    def sync_widget_to_model(self, widget, model_name, origin):
        logging.getLogger(logger).debug(f"Syncing widget {widget} to model {model_name} with origin {origin}")
        widget.setModel(self.widget_models[model_name])

        self.widget_models[model_name].instances.append(WidgetInstance(widget, origin))

        ## TODO: Move the followindb_combo_2 wig to plugins, if only use in specific ones

        if model_name == "db_combo":  ### NO: Cause applies to several plugins
            widget.activated.connect(self.change_selected_db)

        # if model_name in ["image_list", "image_tree"]:
        #    widget.selectionModel().currentChanged.connect(self.select_image)

        # if model_name == "image_tree":
        #    widget.selectionModel().selectionChanged.connect(self.select_images)

        if model_name == "sortby_list":
            widget.activated.connect(self.sort_by_changed)

    ##################################################################################
    ########## Implementation of what-to-do-when-a-widget-emits-signals ##############
    ##################################################################################
    @save_user_config
    def change_selected_db(self, idx):
        if self.raw_image_dbs.items:


            uuid = self.raw_image_dbs.idx_2_uuid(idx)

            db_path = self.raw_image_dbs.items[uuid].info["path"]
            if not os.path.exists(db_path):
                logging.getLogger(logger).warning(f"Database {db_path} not found.")
                show_warning(None, "Warning", f"Database {db_path} not found.")
                return False

            data_dir = self.raw_image_dbs.items[uuid].info["data_dir"]

            self.widget_models["db_combo"].change_selected_db(idx)
            self.raw_image_dbs.current = uuid
            self.img_set.load_db(db_path=db_path, data_dir=data_dir)
            self.widget_models["image_list"].refresh()
            self.widget_models["image_tree"].refresh()

            user_config.set("raw_image_dbs_last", idx)
            self.raw_image_dbs._update.emit()

        return True

    def sort_by_changed(self, index):
        self.sortby = self.widget_models["sortby_list"].sort_keys[index]
        self.widget_models["image_tree"].refresh()

    def select_image(self, index):
        ## TODO: Move to db explorer
        print(
            f"Selected image with UID: {index.data(role=0x0100)} from db: "
            "{self.raw_image_dbs.items[self.raw_image_dbs.current_idx].info}"
        )

    def select_images(self, indices):
        ## TODO: Move to image processor

        self.uuids_selected = set()

        for index in indices:
            if index.data(role=0x0100):
                #self.uuids_selected.append(index.data(role=0x0100))
                self.uuids_selected.add(index.data(role=0x0100))

        self.uuids_selected = list(self.uuids_selected)

        if len(self.uuids_selected) == 0:
            #if len(indices) == 1:
            #for index in indices:
            self.select_images_on_doubleclick(indices)
            print(
                f"Selected image uuids on double click are: {self.uuids_selected}"
            )
        else:
            print(f"Selected image uuids are: {self.uuids_selected}")

    def select_images_on_doubleclick(self, indices):
        ## TODO: Move to image processor
        def get_uuids_from_subtree(index):
            uuids = []
            if index.isValid():
                uuids.append(index.data(role=0x0100))
                for i in range(index.model().rowCount(index)):
                    child_index = index.model().index(i, 0, index)
                    uuids.extend(get_uuids_from_subtree(child_index))

            uuids = [uuid for uuid in uuids if uuid is not None]

            return uuids

        self.uuids_selected = []

        if not isinstance(indices, list):
            indices = [indices]

        for index in indices:
            selected_uuids = get_uuids_from_subtree(index)
            self.uuids_selected.extend(selected_uuids)

        self.uuids_selected = list(set(self.uuids_selected))

    def change_databases(self):
        """Add or remove db from db list"""

        uuid = self.raw_image_dbs.current

        if isinstance(uuid, int) and uuid > 100000:
            uuid = str(uuid)

        if uuid:
            self.img_set.load_db(
                self.raw_image_dbs.items[uuid].info["path"],
                data_dir=self.raw_image_dbs.items[uuid].info["data_dir"],
            )

        self.widget_models["db_combo"].change_databases(self.raw_image_dbs.current_idx)

        self.widget_models["image_list"].refresh()
        self.widget_models["image_tree"].refresh()


class Databases:
    _update: Any

    def __init__(self, name) -> None:
        self.name = name
        self.items = BetterDict(attrs=["uuid", "info"])
        self.current: str | None = None  ## TODO: Turn into namedtuple
        self.current_idx: int | None = 0  ##

    def __len__(self) -> int:
        return len(self.items)

    def initialize(self, _databases) -> None:
        ## TODO: UNUSED ATM ... MAYBE USE BUT REMOVE HARD CODED VALUES
        # _databases = user_config.get("raw_image_dbs")
        if _databases:
            N = 0  # TODO: REMEMBER LATEST
            for uuid, info in _databases.items():
                self.items[uuid] = info
                if N == 0:
                    self.current = uuid
                    self.current_idx = self.uuid_2_idx(uuid)

    @save_user_config
    def add_new_db(self, fp: str, data_dir: Union[str, None] = None) -> bool:
        if os.path.exists(fp):
            if fp not in [_tmp.info["path"] for _tmp in self.items.items()]:
                uuid = helper.create_uuid()
                print(f"Adding database {fp} with uuid {uuid}")

                self.items[str(uuid)] = {"path": fp, "data_dir": data_dir}
                self.current = str(uuid)
                self.current_idx = self.uuid_2_idx(uuid)

                user_config.set(self.name, self.items.as_dict())

                return True

        return False

    @save_user_config
    def remove_db(self, uuid: int, delete_from_disk: bool = False) -> int:
        print(f"Removing database with UUID: {uuid}")
        print(f"from shared data: {self.items.keys()}")

        if delete_from_disk:
            fp = self.items[uuid].info["path"]
            if os.path.exists(fp):
                send2trash(fp)
                logging.getLogger(logger).info(f"Deleted database {fp}")
                ### *.csv.bak staying for the moment

        # if uuid in self.items.keys():
        for idx, key in enumerate(self.items.keys()):
            if key == uuid:
                del self.items[uuid]

                user_config.set(self.name, self.items.as_dict())
                return idx

        return False

    @save_user_config
    def select_db(self, uuid: int) -> None:
        if uuid in self.items:
            self.current = str(uuid)
            self.current_idx = self.uuid_2_idx(uuid)
        else:
            raise ValueError(f"Database with UUID {uuid} not found")

    @overload
    def uuid_2_idx(self, uuid: str) -> int: ...

    @overload
    def uuid_2_idx(self, uuid: int) -> int: ...

    def uuid_2_idx(self, uuid: int | str) -> int:
        if isinstance(uuid, int):
            return list(self.items.keys()).index(str(uuid))
        return list(self.items.keys()).index(uuid)

    def idx_2_uuid(self, idx: int) -> str:
        return list(self.items.keys())[idx]


raw_image_dbs = Databases("raw_image_dbs")
processed_image_dbs = Databases("processed_image_dbs")
