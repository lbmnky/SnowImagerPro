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
from collections import UserDict
from typing import Any

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal as pyqtSignal

from snowimagerpro.app.managers.settings import user_config
from snowimagerpro.app.plugins.base import ModelBase
from snowimagerpro.core import Image


class DataModelSignals(QObject):
    # Emit an "updated" signal when a property changes.
    updated = pyqtSignal()
    refresh_db = pyqtSignal()
    update_dbs = pyqtSignal()
    focus_list = pyqtSignal()
    redraw_img = pyqtSignal()


class DataModel(UserDict):
    def __init__(self, *args, **kwargs):
        self.signals = DataModelSignals()
        self.signals.blockSignals(True)
        super().__init__(*args, **kwargs)

    def post_init(self):
        self.signals.blockSignals(False)

    def do_update(self):
        print(f"do_update not implemented for {self}")


class Model(ModelBase):
    def __init__(self):
        super(Model, self).__init__()
        self.signals = DataModelSignals()
        self.private: dict[str, Any] = {}

    def post_init(self):
        self.private["image"] = Image()
        self.private["defaultDirs"] = user_config.get("inspector.defaultDirs")

        if len(self.private["defaultDirs"]) == 0:
            self.private["defaultDirs"] = [os.path.expanduser("~")]

        self.private["currentDir"] = self.private["defaultDirs"][0]

        self.signals.blockSignals(False)
        self.signals.updated.emit()


model = Model()
