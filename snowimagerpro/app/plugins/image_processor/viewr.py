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

from ast import literal_eval

import pyqtgraph as pg
from numpy import s_ as np_s_
from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QBrush
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTableView,
    QVBoxLayout,
)

import snowimagerpro.core as sipro_core
from snowimagerpro.app.managers import user_config
from snowimagerpro.core.methods import helper

from snowimagerpro.core import DEBUG

from ..base import ViewrBase, getOpenFileName, getSaveFileName, getSaveFileNameMod, show_warning, yes_no_warning

__all__ = ["Viewr", "getOpenFileName", "getSaveFileName", "getSaveFileNameMod", "show_warning", "yes_no_warning"]

class Viewr(ViewrBase, pg.LayoutWidget):
    def __init__(self, image, origin="upper"):
        """Setup view for image of type snowpy.Image."""
        # TODO: add support for stitched images and for images that come as simple np.ndarrays.

        super(Viewr, self).__init__(parent=None)

        self.image = image

        self.win = self.window()
        meta = image._meta

        if isinstance(meta, dict):
            pass
        else:
            meta = meta.to_dict()

        x_size = 800
        y_size = 550

        scale = meta["px_2_mm"]

        plot = pg.PlotItem()
        plot.getAxis("left").setScale(scale)
        plot.getAxis("bottom").setScale(scale)

        imv = pg.ImageView(view=plot)

        if origin == "lower":
            imv.getView().invertY(False)
            slice = np_s_[::-1, :]
        else:
            slice = np_s_[:, :]

        self.img = image._data
        imv.setImage(image._data[slice].T)
        imv.setLevels(0, 1)

        self.addWidget(imv, row=0, col=0, rowspan=1, colspan=1)
        self.imv = imv

        legend = plot.addLegend(brush=pg.mkBrush(0, 0, 0, 180))
        style = pg.PlotDataItem(pen=pg.mkPen(0, 0, 0, 0))
        legend.addItem(style, "0")
        self.label = legend.getLabel(style)

        self.setMouseTracking(True)
        imv.getImageItem().scene().sigMouseMoved.connect(self.onMouseMoved)

        self.px_2_mm = meta["px_2_mm"]

        coords_pix = meta["coords_pix"]
        coords_mm = meta["coords_mm"]

        img_size = sipro_core.methods.get_img_size(image)

        pix_pos = [coords_pix[0] * img_size[0], coords_pix[1] * img_size[1]]
        print("pix pos", pix_pos)
        mm_pos = [coords_mm[0], coords_mm[1]]
        print("mm pos", mm_pos)
        print("scale", scale)

        origin_mm = [0, coords_mm[1] - (img_size[1]-pix_pos[1])*scale]

        self.origin_mm = origin_mm
        print(self.origin_mm, "orig mm")

        meta_table = QTableView()
        model = MetadataTableModel(meta)
        model.dataChanged.connect(self.update_meta)
        meta_table.setModel(model)
        meta_table.setColumnWidth(0, 200)
        meta_table.setColumnWidth(1, x_size - 200)
        # meta_table.update()

        self.addWidget(meta_table, row=3, col=0, rowspan=2, colspan=1)
        self.meta_table = meta_table
        y_size += 200

        try:
            coords_pix = meta["coords_pix"]
            self.add_coords_pix(coords_pix, image)
        except Exception:
            #coords_pix = meta.coords_pix
            pass

        try:
            try:
                ROI = meta["ROI"]
            except Exception:
                ROI = meta.ROI
            self.add_ROI(ROI, sipro_core.methods.get_img_size(image))
        except Exception:
            pass

        self.win.resize(x_size, y_size)

        print("DEBUG, ", DEBUG)
        if DEBUG:
            self.imv.getView().showGrid(True, True)

        self.show()

    def onMouseMoved(self, pos):
        """Plot image value at mouse position to label."""

        data = self.img.T
        img_size = sipro_core.methods.get_img_size(self.image)

        scenePos = self.imv.getImageItem().mapFromScene(pos)
        y, x = int(scenePos.y()), int(scenePos.x())

        offset = self.coords_pix_handle.pos()
        try:
            coords_mm = self.image._meta.coords_mm # for raw images
        except Exception:
            coords_mm = self.image._meta["coords_mm"] # for stitched images

        h = (x-offset[0]) * self.px_2_mm + coords_mm[0] #+ self.origin_mm[0]
        #v = (img_size[1] - y) * self.px_2_mm + self.origin_mm[1]
        v = (y-offset[1]) * self.px_2_mm + coords_mm[1] #- self.origin_mm[1]


        if len(data.shape) == 3:
            _, nCols, nRows = data.shape
            if (x < 0) or (x >= nCols) or (y < 0) or (y >= nRows):
                z = "Out of bounds"
            else:
                z = data[:, int(x), int(y)]
                z = f"R: {z[0]:.2f}, G: {z[1]:.2f}, B: {z[2]:.2f}"

        elif len(data.shape) == 2:
            nCols, nRows = data.shape
            if (x < 0) or (x >= nCols) or (y < 0) or (y >= nRows):
                z = "Out of bounds"
            else:
                z = data[int(x), int(y)]
                z = f"{z:.2f}"
        else:
            z = "Not supported"

        self.label.setText(f"Pix: {x, y} | Pos: {h:.2f}, {v:.2f} | Value: {z}")

    def add_coords_pix(self, coords, img, color="g"):
        img_size = sipro_core.methods.get_img_size(img)

        if not img_size:
            return

        point_px = [coords[0] * img_size[0], coords[1] * img_size[1]]

        point_handle = pg.TargetItem(
            point_px,
            size=15,
            pen=pg.mkPen(color, width=1),
            brush=(255, 255, 255, 0),
            hoverPen=pg.mkPen(color, width=2),
            hoverBrush=(255, 255, 255, 0),
        )

        point_handle.sigPositionChangeFinished.connect(
            lambda val, img=img: self.update_coords_pix(val, img)
        )

        self.imv.addItem(point_handle)
        self.coords_pix_handle = point_handle

    def add_ROI(self, ROI, img_size):
        ROI_colors = [
            "green",
            "red",
        ]  # green: gray target, red: white target (for contrast reasons)
        ROI_handles = []
        TEXT_handles = []

        for i, roi in enumerate(ROI):
            color = ROI_colors[i]
            n_targets = len(roi)
            roi_handles = []
            text_handles = []

            for j in range(n_targets):
                pos, size = sipro_core.methods.ROI_pos_to_size(roi[j], img_size)
                roi_handle = pg.RectROI(pos, size, pen=(color))

                roi_handle.sigRegionChangeFinished.connect(
                    lambda roi,
                    handle=roi_handle,
                    img_size=img_size,
                    idx=(i, j): self.update_roi(roi, handle, img_size, idx)
                )

                roi_handles.append(roi_handle)
                self.imv.addItem(roi_handle)

                avs = sipro_core.methods.average_in_ROI(self.img, [roi[j]])[0]

                text = pg.TextItem(
                    ", ".join(str(round(av, 3)) for av in avs),
                    color="k",
                    fill=pg.mkBrush((255, 255, 255, 175)),
                )
                self.imv.addItem(text)
                text.setPos(pos[0] + size[0], pos[1])
                text_handles.append(text)

            ROI_handles.append(roi_handles)
            TEXT_handles.append(text_handles)

        self.ROI_handles = ROI_handles
        self.TEXT_handles = TEXT_handles

    def update_coords_pix(self, val, img):
        img_size = sipro_core.methods.get_img_size(img)

        if not img_size:
            return

        self.image._meta["coords_pix"] = [
            round(px / img_size[i], 5) for i, px in enumerate(list(val.pos()))
        ]

        print("Updating coords_pix")
        print(self.image._meta["coords_pix"])

        # plugins.redraw_viewr(self)

        self.meta_table.model().df = self.image._meta

    # TODO: move to parent if used identically in multiple views
    def update_roi(self, roi, handle, img_size, idx):
        """Update ROI in image and update text item with average values."""

        x0 = roi.pos().x() / img_size[0]
        y0 = roi.pos().y() / img_size[1]
        x1 = x0 + roi.size().x() / img_size[0]
        y1 = y0 + roi.size().y() / img_size[1]

        if x0 < 0:
            x0 = 0
            handle.setPos([0, roi.pos().y()])

        if y0 < 0:
            y0 = 0
            handle.setPos([roi.pos().x(), 0])

        if x1 > 1:
            x1 = 1
            handle.setSize([(1 - x0) * img_size[0], roi.size().y()])

        if y1 > 1:
            y1 = 1
            handle.setSize([roi.size().x(), (1 - y0) * img_size[1]])

        self.image._meta.ROI[idx[0]][idx[1]] = [[x0, y0], [x1, y1]]

        avs = sipro_core.methods.average_in_ROI(self.image._data, [[[x0, y0], [x1, y1]]])[0]
        self.TEXT_handles[idx[0]][idx[1]].setPos(
            roi.pos().x() + roi.size().x(), roi.pos().y()
        )
        self.TEXT_handles[idx[0]][idx[1]].setText(
            ", ".join(str(round(av, 3)) for av in avs)
        )

        # plugins.redraw_viewr(self)

    def redraw(self):
        img_size = sipro_core.methods.get_img_size(self.image)

        pos = (
            self.image._meta.coords_pix[0] * img_size[0],
            self.image._meta.coords_pix[1] * img_size[1],
        )

        self.coords_pix_handle.setPos(pos)

        for i, roi in enumerate(self.image._meta.ROI):
            for j, target in enumerate(roi):
                pos, size = sipro_core.methods.ROI_pos_to_size(target, img_size)
                self.ROI_handles[i][j].setPos(pos)
                self.ROI_handles[i][j].setSize(size)

                avs = sipro_core.methods.average_in_ROI(self.image._data, [target])[0]
                self.TEXT_handles[i][j].setPos(pos[0] + size[0], pos[1])
                self.TEXT_handles[i][j].setText(
                    ", ".join(str(round(av, 3)) for av in avs)
                )

    def update_meta(self):
        print(self.image._meta["coords_mm"])

        idx = self.meta_table.model()._data[0].index("coords_mm")
        coords_mm = self.meta_table.model()._data[1][idx]

        print(coords_mm)
        self.image._meta["coords_mm"] = literal_eval(coords_mm)


class MetadataTableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)

        self._data = self.extract_data(data)

        self._editable = [
            i
            for i, item in enumerate(self._data[0])
            if item in ["coords_mm", "stitch_at_mm", "comment"]
        ]

    def extract_data(self, data):
        if isinstance(data, sipro_core.ImageMetadata):
            return [data.to_key_list(), data.to_list()]
        elif isinstance(data, dict):
            return [list(data.keys()), list(data.values())]
        else:
            print("MetadataTableModel: Data type not supported")

    @property
    def df(self):
        return self._data

    @df.setter
    def df(self, df):
        self.beginResetModel()

        self._data = self.extract_data(df)
        self.endResetModel()

    def columnCount(self, parent):
        return 2

    def rowCount(self, parent):
        return len(self._data[0])

    def flags(self, index):
        if index.column() == 1 and index.row() in self._editable:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data[index.column()][index.row()] = value
            self.dataChanged.emit(index, index)
            return True

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data[index.column()][index.row()]
                return str(value)
            elif role == Qt.BackgroundRole:
                if index.row() in self._editable and index.column() == 0:
                    return QBrush(Qt.darkCyan)


from .model import model


class AddToDatabaseDialog(QDialog):
    def __init__(self):
        super(AddToDatabaseDialog, self).__init__()

        self.setWindowTitle("Add to database")
        self.setWindowFlags(Qt.Window)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select database?"))

        listWidget = QListWidget()
        listWidget.setSelectionMode(QListWidget.ExtendedSelection)

        dbs = model.public.processed_image_dbs.items

        print(dbs)

        for entry in dbs.items():
            uuid, info = entry
            name = info["path"].split("/")[-1]
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, uuid)
            listWidget.addItem(item)

        self.listWidget = listWidget

        layout.addWidget(listWidget)

        add_btn = QPushButton("Add")
        layout.addWidget(add_btn)
        add_btn.clicked.connect(self.add_to_db)
        add_btn.setDisabled(True)
        self.add_btn = add_btn

        cancel_btn = QPushButton("Cancel")
        layout.addWidget(cancel_btn)
        cancel_btn.clicked.connect(self.close)

        self.setLayout(layout)

        self.img_fp = None

    def add_fp(self, fp):
        print("filepath is ", fp)
        self.add_btn.setEnabled(True)

        self.img_fp = fp[0]

    def add_to_db(self):
        db_items = self.listWidget.selectedItems()

        new_uuid = helper.create_uuid()
        print(f"new uid: {new_uuid}")

        # dbs = user_config.get("processed_image_dbs")
        dbs = model.public.processed_image_dbs.items

        for db in db_items:
            print(db.text())
            uuid = db.data(Qt.UserRole)

            db_entry = dbs[uuid]
            print(dbs)
            print(uuid)
            print(db_entry)
            fp = db_entry.info["path"]

            with open(fp, "a") as f:
                print(f"Adding {self.img_fp} to {fp}")
                f.write(f"{new_uuid},{str(self.img_fp)}\n")

        model.public.processed_image_dbs._update.emit()

        self.close()
