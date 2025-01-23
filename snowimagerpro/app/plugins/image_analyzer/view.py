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

from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem, QWidget

from snowimagerpro.app.managers.paths import paths
from snowimagerpro.app.managers.settings import user_config
from snowimagerpro.app.plugins.base import ViewBase

from .logic import logic
from .model import model
from .ui.ctrls_ui import Ui_Form as ctrls_ui
from .ui.explr_ui import Ui_Form as explr_ui
from .viewr import getOpenFileName


def add_h5_to_db():
    fp = getOpenFileName(
        None, "Open File", user_config.get("analyzer.db_path"), "HDF5 (*.h5)"
    )
    logic.add_h5_to_db(fp)


def add_db():
    db_path = user_config.get("analyzer.db_path")
    fp = getOpenFileName(None, "Open File", db_path, "CSV (*.csv)")
    logic.add_db(fp)
    user_config.set("analyzer.db_path", str(Path(fp).parent))


def remove_db():
    idx = view.explr._ui.cb_change_db.currentIndex()
    uuid = view.explr._ui.cb_change_db.itemData(idx)
    logic.remove_db(uuid)


def change_data_dir(current_data_dir):
    new_data_dir = QFileDialog.getExistingDirectory(
        None, "Select Directory", current_data_dir
    )
    return new_data_dir


class View(ViewBase):
    def __init__(self):
        super(View, self).__init__()
        self._name = "image analyzer"

    def initialize(self):
        self.ctrls = Ctrls()
        self.explr = Explr()

        self._icon = paths.resource("icons/analysis.svg")

        model.public.sync_widget_to_model(
            self.explr._ui.cb_change_db, "db_combo_2", "image_analyzer"
        )

        for instance in model.public.widget_models["db_combo_2"].instances:
            if instance.origin == "image_analyzer":
                instance.widget.activated.connect(self.on_db_changed)

        model.signals.update_ui.connect(self.on_update_ui)
        model.public.processed_image_dbs._update.connect(
            self.on_image_added_from_processor
        )

        logic.change_db(0)

        model.post_init()

    def on_db_changed(self, index):
        logic.change_db(index)

    def on_image_added_from_processor(self):
        idx = model.public.processed_image_dbs.current_idx
        logic.change_db(idx)

    def on_update_ui(self):
        self.explr._ui.treeWidget.clear()
        # for uuid, path in model.private["processed_image_db"].items():
        for uuid, path in model.public.processed_images_db.items():
            item = QTreeWidgetItem(self.explr._ui.treeWidget)
            item.setText(0, path)
            item.setText(1, "")

        self.explr._ui.le_data_directory.clear()
        if model.public.processed_image_dbs.current is not None:
            data_dir = model.public.processed_image_dbs.items[
                model.public.processed_image_dbs.current
            ].info["data_dir"]
            self.explr._ui.le_data_directory.setText(data_dir)


class Ctrls(QWidget):
    def __init__(self):
        super().__init__()

        self._ui = ctrls_ui()
        self._ui.setupUi(self)

        self._ui.btn_add_h5.clicked.connect(add_h5_to_db)

        self._ui.btn_add_db.clicked.connect(add_db)
        self._ui.btn_rmv_db.clicked.connect(remove_db)

        self._ui.btn_calc_SSA.clicked.connect(logic.calc_SSA)
        self._ui.btn_calc_rho.clicked.connect(logic.calc_rho)

        self._ui.btn_prnt_rep.clicked.connect(logic.save_report)
        self._ui.btn_close_views.clicked.connect(logic.close_views)


class Explr(QWidget):
    def __init__(self):
        super().__init__()

        self._ui = explr_ui()
        self._ui.setupUi(self)

        self._ui.treeWidget.itemSelectionChanged.connect(self.on_select_images)
        self._ui.treeWidget.itemDoubleClicked.connect(self.on_double_click)

        self._ui.btn_change_data_dir.clicked.connect(self.on_change_data_dir)

    def on_change_data_dir(self):
        uuid = model.public.processed_image_dbs.current
        if uuid is not None:
            current_data_dir = model.public.processed_image_dbs.items[uuid].info[
                "data_dir"
            ]
            new_data_dir = change_data_dir(current_data_dir)
            if new_data_dir:
                self._ui.le_data_directory.setText(new_data_dir)
                logic.change_data_dir(uuid, new_data_dir)

    def on_select_images(self):
        items = self._ui.treeWidget.selectedItems()
        print(items)

    def on_double_click(self, item, column):
        fp = item.text(0)
        print(fp, column)

        logic.load(fp)


view = View()
