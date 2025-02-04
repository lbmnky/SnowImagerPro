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

from itertools import groupby

from PySide6 import QtCore

from snowimagerpro.core.metadata import ImageMetadata
from snowimagerpro.app.managers import user_config


class DatabasesListModel(QtCore.QStringListModel):
    """DB list model for combobox and editable combobox"""

    def __init__(self, model, parent=None):
        QtCore.QStringListModel.__init__(self, parent)
        self.model = model
        self.instances = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.model)

    def data(self, index, role):
        if len(self.model) == 0:
            return
        if (
            not index.isValid() or index.row() >= self.rowCount()
        ):  ## FIX: IndexError: list index out of range
            ## Occurs when a database is removed
            return
        if role == QtCore.Qt.UserRole:
            return self.model.items[index.row()].uuid
        if role == QtCore.Qt.DisplayRole:
            return str(self.model.items[index.row()].info["path"])

        return QtCore.QStringListModel.data(self, index, role)

    def change_selected_db(self, index):
        for instance in self.instances:
            instance.widget.setCurrentIndex(index)

            idx = self.createIndex(index, 0)
            if instance.widget.isEditable():
                instance.widget.setCurrentText(self.data(idx, QtCore.Qt.DisplayRole))

    def change_databases(self, index):
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        for instance in self.instances:
            instance.widget.setCurrentIndex(index)

        idx = self.createIndex(index, 0)
        for instance in self.instances:
            if instance.widget.isEditable():
                instance.widget.setCurrentText(self.data(idx, QtCore.Qt.DisplayRole))


class DatabasesListModel_2(QtCore.QStringListModel):
    """DB list model for combobox and editable combobox"""

    ##### OBSOLETED #####

    def __init__(self, model, parent=None):
        QtCore.QStringListModel.__init__(self, parent)
        self.model = model
        self.instances = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.model.processed_image_dbs)

    def data(self, index, role):
        if len(self.model.processed_image_dbs) == 0:
            return
        if (
            not index.isValid() or index.row() >= self.rowCount()
        ):  ## FIX: IndexError: list index out of range
            ## Occurs when a database is removed
            return
        if role == QtCore.Qt.UserRole:
            return self.model.processed_image_dbs.items[index.row()].uuid
        if role == QtCore.Qt.DisplayRole:
            return str(self.model.processed_image_dbs.items[index.row()].info["path"])

        return QtCore.QStringListModel.data(self, index, role)

    def change_selected_db(self, index):
        for instance in self.instances:
            instance.widget.setCurrentIndex(index)

            idx = self.createIndex(index, 0)
            if instance.widget.isEditable():
                instance.widget.setCurrentText(self.data(idx, QtCore.Qt.DisplayRole))

    def change_databases(self, index):
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        for instance in self.instances:
            instance.widget.setCurrentIndex(index)

        idx = self.createIndex(index, 0)
        for instance in self.instances:
            if instance.widget.isEditable():
                instance.widget.setCurrentText(self.data(idx, QtCore.Qt.DisplayRole))


class ImageDBListModel(QtCore.QStringListModel):
    def __init__(self, model, parent=None):
        QtCore.QStringListModel.__init__(self, parent)
        self.model = model
        self.instances = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.model._image_db)

    def data(self, index, role):
        if index.isValid():
            keys = list(self.model._image_db)
            key = keys[index.row()]

            if role == QtCore.Qt.DisplayRole:
                return self.model._image_db[key].filepath.stem

            if role == QtCore.Qt.UserRole:
                return str(self.model._image_db[key].ID)

            return QtCore.QStringListModel.data(self, index, role)

    def rowInserted(self, parent, start, end):
        self.beginInsertRows(parent, start, end)
        self.endInsertRows()

    def refresh(self):
        for instance in self.instances:
            instance.widget.dataChanged(QtCore.QModelIndex(), QtCore.QModelIndex())


class TreeItem(object):
    def __init__(self, _name, _parent=None, _uuid=None):
        self._name = _name
        self._uuid = _uuid
        self._children = []
        self._parent = _parent

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def uuid(self):
        return self._uuid

    def add_uuid(self, uuid):
        self._uuid = uuid

    def child(self, row):
        return self._children[row]

    def child_count(self):
        return len(self._children)

    def parent(self):
        try:
            return self._parent
        except AttributeError:
            return None

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def add_child(self, child):
        self._children.append(child)

    def insert_child(self, position, child):
        if position < 0 or position > len(self._children):
            return False

        self._children.insert(position, child)
        child._parent = self
        return True

    def remove_child(self, position):
        if position < 0 or position > len(self._children):
            return False

        child = self._children.pop(position)
        child._parent = None

        return True

    def log(self, tab_level=-1):
        output = ""
        tab_level += 1

        for i in range(tab_level):
            output += "\t"

        output += "|------" + self._name + "\n"

        for child in self._children:
            output += child.log(tab_level)

        tab_level -= 1
        output += "\n"

        return output

    def __repr__(self):
        return self.log()


class ImageDBTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, model, _parent=None):
        super(ImageDBTreeModel, self).__init__(_parent)

        self.model = model
        self.instances = []

        self.root_item = TreeItem("ROOT")

        self._data = {}

    def db_to_tree(self, db, sortby="date"):
        """
        Convert the database to a tree structure
        """

        if sortby == "date":
            by_first = ImageMetadata.by_date
            by_second = ImageMetadata.by_location
        elif sortby == "location":
            by_first = ImageMetadata.by_location
            by_second = ImageMetadata.by_date
        else:
            raise ValueError("Invalid sortby. Must be 'date' or 'location'")

        user_config.set("processor.sortby", sortby)

        _data = {}
        for first, after_first in groupby(db, by_first):
            _data[first] = {}
            for second, after_second in groupby(after_first, by_second):
                _data[first][second] = {}

                for meas_group, after_meas_group in groupby(
                    sorted(after_second, key=ImageMetadata.by_meas_group),
                    ImageMetadata.by_meas_group,
                ):
                    _data[first][second][meas_group] = {}

                    after_meas_group = sorted(
                        after_meas_group, key=ImageMetadata.by_img_type
                    )

                    for img_type, after_img_type in groupby(
                        after_meas_group, ImageMetadata.by_img_type
                    ):
                        _data[first][second][meas_group][img_type] = {}
                        for image in after_img_type:
                            _data[first][second][meas_group][img_type][
                                image.filepath.stem
                            ] = str(image.ID)

        return _data

    def refresh(self):
        image_db = self.model.img_set._image_db.values()

        self._data = self.db_to_tree(image_db, sortby=self.model.sortby)

        self.root_item = TreeItem("ROOT")
        self.setup_model_data(self._data)

        self.layoutChanged.emit()
        for i in self.instances:
            i[0].expandToDepth(2)

    def setup_model_data(self, _data, _parent=None):
        if _parent is None:
            _parent = self.root_item

        for key, value in sorted(_data.items()):
            if isinstance(value, dict):
                _item = TreeItem(key, _parent)
                _parent.add_child(_item)
                self.setup_model_data(value, _item)
            if isinstance(value, str):
                _item = TreeItem(key, _parent, _uuid=value)
                _parent.add_child(_item)

    def rowCount(self, parent):
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.child_count()

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return item.name()

        if role == QtCore.Qt.UserRole:
            if index.column() == 0:
                return item.uuid()

        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                item = index.internalPointer()
                item.set_name(value)
                self.dataChanged.emit(index, index)
                return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return self.root_item.name()
            else:
                return "Typeinfo"

    def flags(self, index):
        return (
            QtCore.Qt.ItemIsEnabled
            | QtCore.Qt.ItemIsSelectable
            | QtCore.Qt.ItemIsEditable
        )

    def parent(self, index):
        item = self.get_item(index)

        try:
            parent_item = item.parent()
        except AttributeError:
            return QtCore.QModelIndex()

        if parent_item == self.root_item:
            return QtCore.QModelIndex()

        if parent_item is None:
            return QtCore.QModelIndex()

        if parent_item.row() is None:
            return QtCore.QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def index(self, row, column, parent):
        parent_item = self.get_item(parent)

        child_item = parent_item.child(row)

        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()

    def get_item(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.root_item

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parent_item = self.get_item(parent)
        success = False

        self.beginInsertRows(parent, position, position + rows - 1)

        for row in range(rows):
            child_count = parent_item.child_count()
            child_item = TreeItem("untitled" + str(child_count))
            success = parent_item.insert_child(position, child_item)

        self.endInsertRows()

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parent_item = self.get_item(parent)
        success = False

        self.beginRemoveRows(parent, position, position + rows - 1)

        for row in range(rows):
            success = parent_item.remove_child(position)

        self.endRemoveRows()

        return success


class SortbyListModel(QtCore.QStringListModel):
    def __init__(self, model, parent=None):
        QtCore.QStringListModel.__init__(self, parent)
        self.model = model
        self.sort_keys = ["date", "location"]
        self.instances = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.sort_keys)

    def data(self, index, role):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return self.sort_keys[index.row()]

            return QtCore.QStringListModel.data(self, index, role)

    # def update(self):
    #    for i in self.instances:
    #        i.dataChanged(QtCore.QModelIndex(), QtCore.QModelIndex())
