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

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget

from snowimagerpro.app.managers.data import PublicDataModel
from snowimagerpro.app.managers.paths import paths

import snowimagerpro.core as sipro_core

from .shared_ui_elements import (
    DatabasesListModel,
    ImageDBListModel,
    ImageDBTreeModel,
    SortbyListModel,
)


class LogicBase(QObject):
    update = Signal(object)
    progress = Signal(int)
    update_view = Signal()

    def __init__(self, fp=__file__):
        super(LogicBase, self).__init__()
        self.views = []

    def do_update(self):
        print(f"do_update not implemented for {self}")

    def remove_view(self, view):
        # assert self.views is not None
        view.close()
        self.views = [i for i in self.views if i != view]
        logging.info("Closed 1 view")

    def toggle_debug(self, *args):
        sipro_core.toggle_debug()


    def close_views(self):
        N = 0
        for view in self.views:
            N += 1
            self.remove_view(view)


class ViewBase(QObject):
    def __init__(self, fp=__file__):
        super(ViewBase, self).__init__()

        self._icon = paths.resource("icons/db.svg")


public_data = PublicDataModel(
    widget_models={
        "db_combo": DatabasesListModel,  # --> These two share same model class
        "db_combo_2": DatabasesListModel,  # -/
        #
        "image_tree": ImageDBTreeModel,
        "image_list": ImageDBListModel,
        "sortby_list": SortbyListModel,
        #
    }
)


class ModelBase(QObject):
    update1 = Signal()
    update2 = Signal()

    def __init__(self) -> None:
        super().__init__()

        # public scope is shared between plugins
        self.public = public_data
        self.public.raw_image_dbs._update = self.update1
        self.public.processed_image_dbs._update = self.update2

        # private scope is unique to each plugin
        # self.private: dict[str, Any] = {}
        # REQUIRE TO IMPLEMENT IN EACH PLUGIN

    def do_update(self):
        self.public.change_databases()
        print(f"do_update not implemented for {self}")


class ViewrBase(QWidget):
    """Base class for Viewr! Viewr shows data as a popup window
    or within the UI and is part of View class.

    Child class inside a plugin should override `show` method to display
    data, but call `super(ChildClass, self).show()` at the end to show the
    Qt window, e.g.:

    def show(self, data):               <- Override show
        if isinstance(data, ndarray):   <- Handle different data types
            self.show_img(data)         <- Impl. for image data
        elif isinstance(data, list):
            self.show_profile(data)     <- Impl. for profile data
        else:
            pass                        <- Handle other data types
        super(ChildClass, self).show()  <- Show the Qt window

    """

    closed = Signal(object)

    def __init__(self, parent=None):
        super(ViewrBase, self).__init__()

    def redraw(self):
        print("Redraw not implemented in", self)

    def closeEvent(self, event):
        self.closed.emit(self)
        super().closeEvent(event)


def getOpenFileName(*args):
    fp = QFileDialog.getOpenFileName(*args)
    return fp[0]


def getSaveFileName(*args):
    fp = QFileDialog.getSaveFileName(*args)
    if fp[0] == "":
        return None
    return fp[0]


# TODO: Gotta check this on Mac
def getSaveFileNameMod(*args, custom_file_name=None):
    dlg = QFileDialog(*args)
    dlg.setAcceptMode(QFileDialog.AcceptSave)
    dlg.setOption(QFileDialog.DontUseNativeDialog, True)
    if custom_file_name:
        dlg.layout().itemAt(4).widget().setText(custom_file_name)
    if dlg.exec() == QFileDialog.Accepted:
        return dlg.selectedFiles()[0]
    return None

def getFileName(*args):
    dlg = QFileDialog(*args)
    dlg.setOption(QFileDialog.DontUseNativeDialog, True)
    dlg.exec()  # Just ignore XCB warning
    return dlg.selectedFiles()[0]


def show_warning(*args):
    QMessageBox.warning(*args)


def yes_no_warning(*args):
    ret = QMessageBox.question(*args, QMessageBox.Yes | QMessageBox.No)
    if ret == QMessageBox.Yes:
        return True
    else:
        return False
