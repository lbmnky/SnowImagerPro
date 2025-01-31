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

import re

from PySide6.QtWidgets import (
    QMessageBox,
    QFileDialog,
    QListView,
    QTreeView,
    QAbstractItemView,
)


def show_warning(*args):
    QMessageBox.warning(*args)


def select_folders(*args):

    def fv_double_clicked(index):
        dlg.selectFile("")

    dlg = QFileDialog(*args)
    dlg.setFileMode(QFileDialog.Directory)
    dlg.setOption(QFileDialog.DontUseNativeDialog, True)
    file_view = dlg.findChild(QListView, "listView")

    if file_view:
        file_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

    f_tree_view = dlg.findChild(QTreeView)

    if f_tree_view:
        f_tree_view.setSelectionMode(QAbstractItemView.MultiSelection)

    # TODO: Eliminate parent folder element from dlg.selectedFiles() list more elegantly
    # FIX below
    if dlg.exec():
        selected = dlg.selectedFiles()
        if len(selected) == 1:
            return selected[0]
        elif len(selected) > 1:
            for s in selected:
                print(s.split("/")[-1])
                if not re.match(r"\d{4}-\d{2}-\d{2}*", s.split("/")[-1]):
                    selected.remove(s)

        return dlg.selectedFiles()[1:]
