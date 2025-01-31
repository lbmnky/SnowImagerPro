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
from pathlib import Path

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

    dlg = QFileDialog(*args)
    dlg.setFileMode(QFileDialog.Directory)
    dlg.setOption(QFileDialog.DontUseNativeDialog, True)

    # TODO: Toggle selection mode based on selection, to allow adding folders or files
    #def toggle_file_mode(info):
    #    print(info)
    #    if info.isFile():
    #        dlg.setFileMode(QFileDialog.ExistingFiles)
    #    elif info.isDir():
    #        dlg.setFileMode(QFileDialog.Directory)
    #dlg.currentChanged.connect(toggle_file_mode)

    file_view = dlg.findChild(QListView, "listView")

    if file_view:
        file_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

    f_tree_view = dlg.findChild(QTreeView)

    if f_tree_view:
        f_tree_view.setSelectionMode(QAbstractItemView.MultiSelection)

    if dlg.exec():
        selected = dlg.selectedFiles()

        # Return files only if any files are selected
        if any(Path(s).is_file() for s in selected):
            selected = [s for s in selected if Path(s).is_file()]
            return selected, None

        # return list of folders otherwise
        # need to return first/parent folder # TODO: Fix this?
        if len(selected) > 1:
            for s in selected:
                if not re.match(r"\d{4}-\d{2}-\d{2}", Path(s).stem): # WHAT IF FILENAME FORMAT CHANGES? # TODO: check Win/Mac
                    selected.remove(s)

        # Otherwise return the one selected folder
        return None, selected

    return None, None
