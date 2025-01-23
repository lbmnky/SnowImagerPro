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

from collections import UserDict
from typing import Any

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal as pyqtSignal

from snowimagerpro.app.plugins.base import ModelBase


class DataModelSignals(QObject):
    # Emit an "updated" signal when a property changes.
    change_img = pyqtSignal()
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
        self.signals.blockSignals(False)


model = Model()
