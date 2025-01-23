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

from PySide6.QtWidgets import QFileSystemModel, QHeaderView, QWidget

from snowimagerpro.app.managers.paths import paths
from snowimagerpro.app.plugins.base import ViewBase

from .logic import logic
from .model import model
from .ui.ctrls_ui import Ui_Form as ctrls_ui
from .ui.explr_ui import Ui_Form as explr_ui


class View(ViewBase):
    def __init__(self):
        super(View, self).__init__()
        self._name = "image inspector"

    def initialize(self):
        self.ctrls = Ctrls()
        self.explr = Explr()

        self._icon = paths.resource("icons/inspecting.svg")

        self.ctrls._ui.btn_load.clicked.connect(logic.load)
        self.ctrls._ui.btn_close_views.clicked.connect(logic.close_views)

        self.ctrls._ui.btn_add_def_dir.clicked.connect(self.do_add_default_dir)
        self.ctrls._ui.btn_rmv_def_dir.clicked.connect(self.do_rmv_default_dir)

        self.explr._ui.treeView.doubleClicked.connect(self.do_load)
        self.explr._ui.comboBox.activated.connect(self.do_update_model)

        model.signals.updated.connect(self.update_ui)

    def do_load(self):
        fp = self.explr.fs_model.filePath(self.explr._ui.treeView.selectedIndexes()[0])
        logic.load(fp)

    def do_update_model(self, idx):
        current_text = self.explr._ui.comboBox.currentText()
        logic.update_model(idx, current_text)

    def do_add_default_dir(self, idx):
        current_text = self.explr._ui.comboBox.currentText()
        logic.add_default_dir(current_text)

    def do_rmv_default_dir(self, idx):
        current_text = self.explr._ui.comboBox.currentText()
        logic.rmv_default_dir(current_text)

    def update_ui(self):
        self.explr.update_fs_model(model.private["currentDir"])
        self.explr.set_default_dirs(
            model.private["defaultDirs"], model.private["currentDir"]
        )


class Ctrls(QWidget):
    def __init__(self):
        super().__init__()

        self._ui = ctrls_ui()
        self._ui.setupUi(self)


class Explr(QWidget):
    def __init__(self):
        super().__init__()

        self._ui = explr_ui()
        self._ui.setupUi(self)

        fs_model = QFileSystemModel()  # TODO: Not working
        fs_model.setNameFilters(["*.dng", "*.bay", "*.raw"])
        self.fs_model = fs_model

    def set_default_dirs(self, dirs, curr_dir):
        self._ui.comboBox.clear()
        self._ui.comboBox.addItems(dirs)
        self._ui.comboBox.setCurrentText(curr_dir)

    def update_fs_model(self, curr_dir):
        fs_model = self.fs_model
        fs_model.setRootPath(curr_dir)

        self._ui.treeView.setModel(fs_model)
        self._ui.treeView.setRootIndex(fs_model.index(curr_dir))
        self._ui.treeView.header().setSectionResizeMode(0, QHeaderView.Stretch)


view = View()
