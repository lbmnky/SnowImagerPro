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

import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFileDialog,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from snowimagerpro.app.popups import select_folders

from snowimagerpro.app.managers.paths import paths
from snowimagerpro.app.managers.settings import user_config
from snowimagerpro.app.plugins.base import ViewBase
from snowimagerpro.core.metadata import ImageMetadata
from snowimagerpro.core.methods import processing as pro

from .logic import logic
from .model import model
from .ui.ctrls_ui import Ui_Form as ctrls_ui
from .ui.explr_ui import Ui_Form as explr_ui
from .viewr import Viewr, getFileName, yes_no_warning




def add_images_to_db():
    files, folders = select_folders(
        None,
        "Select image directories",
    )
    print("files", files)
    print("folders", folders)
    logic.add_images_to_db(files, folders)

def remove_image_from_db():
    indices = view.explr._ui.listView.selectionModel().selectedRows()
    uuids = []
    for idx in indices:
        print(idx)
        uuid = view.explr._ui.listView.model().data(idx, role=0x0100)
        uuids.append(uuid)
    logic.remove_images_from_db(uuids)


def copy_metadata():
    print("copy metadata")
    dlg = settings_dialog
    dlg.exec()


def paste_metadata():
    selected = view.explr._ui.listView.selectionModel().selectedRows()
    uuids = []
    for idx in selected:
        uuid = view.explr._ui.listView.model().data(idx, role=0x0100)
        uuids.append(uuid)

    logic.paste_metadata(uuids)


def add_db():
    db_path = user_config.get("explorer.db_path")
    fp = getFileName(None, "Open File", db_path, "CSV (*.csv)")
    if not Path(fp).exists():
        if Path(fp).suffix in [".csv", ""]:
            if Path(fp).suffix == "":
                fp = fp + ".csv"
            create_db(fp)
        else:
            return

    user_config.set("explorer.db_path", str(Path(fp).parent))

    logic.add_db(fp)


def create_db(fp):
    assert fp.endswith(".csv") or fp.endswith("")
    with open(fp, "w") as f:
        f.write(",".join(ImageMetadata.to_key_list()) + "\n")


def remove_db():
    idx = view.explr._ui.comboBox.currentIndex()
    uuid = view.explr._ui.comboBox.itemData(idx)
    logic.remove_db(uuid)


def delete_db():
    flag = yes_no_warning(
        None, "Delete DB", "Are you sure you want to delete the selected DB?"
    )
    print("flag", flag)
    if flag:
        idx = view.explr._ui.comboBox.currentIndex()
        uuid = view.explr._ui.comboBox.itemData(idx)
        logic.delete_db(uuid)
    else:
        print("Deletion cancelled")


def select_db(idx):
    uuid = view.explr._ui.comboBox.itemData(idx)
    logic.select_db(uuid)


def change_data_dir(curr_data_dir):
    new_data_dir = QFileDialog.getExistingDirectory(
        None,
        "Open a folder",
        curr_data_dir,
    )
    return new_data_dir


class View(ViewBase):
    def __init__(self):
        super(View, self).__init__()
        self._name = "db explorer"

        model.signals.update_dbs.connect(self.do_update)

        model.post_init()

    def initialize(self):
        self.ctrls = Ctrls()
        self.explr = Explr()

        settings_dialog.initialize()

        self._icon = paths.resource("icons/exploring.svg")

        self.explr._ui.listView.setDragEnabled(False)

        self.ctrls._ui.checkBox_autosave.checkStateChanged.connect(self.toggle_autosave)

        model.public.sync_widget_to_model(
            self.explr._ui.comboBox, "db_combo", "db_explorer"
        )
        model.public.sync_widget_to_model(
            self.explr._ui.listView, "image_list", "db_explorer"
        )

        model.signals.change_img.connect(self.change_img)

    def post_init(self):
        print("post_init IS implemnted for db_explorer (view)")

        model.public.raw_image_dbs._update.connect(self.do_update)

        for instance in model.public.widget_models["image_list"].instances:
            if instance.origin == "db_explorer":
                instance.widget.selectionModel().currentChanged.connect(
                    self.on_listView_clicked
                )

        for instance in model.public.widget_models["image_tree"].instances:
            if instance.origin != "db_explorer":
                instance.widget.selectionModel().currentChanged.connect(
                    self.on_listView_clicked
                )

        uuid = model.public.raw_image_dbs.current
        if uuid:
            current_data_dir = model.public.raw_image_dbs.items[uuid].info["data_dir"]
            self.explr._ui.le_data_directory.setText(current_data_dir)

    def do_update(self):
        uuid = model.public.raw_image_dbs.current
        if uuid:
            current_data_dir = model.public.raw_image_dbs.items[uuid].info["data_dir"]

            if not current_data_dir:
                current_data_dir = ""

            self.explr._ui.le_data_directory.setText(current_data_dir)
            model.public.img_set._data_dir = current_data_dir

            self.explr.update_view()

    def toggle_autosave(self, state):
        if state == Qt.Checked:
            user_config.set("explorer.autosave", True)
            self.ctrls._ui.btn_write_to_curr_db.setEnabled(False)
            model.public.img_set.autosave_on = True
        else:
            user_config.set("explorer.autosave", False)
            self.ctrls._ui.btn_write_to_curr_db.setEnabled(True)
            model.public.img_set.autosave_on = False

    def change_img(self):
        # self.setParametersEnabled(False)
        self.explr.show_selected(
            model.private["current_img"], model.private["current_db_entry"]
        )
        # self.setParametersEnabled(True)

    def on_listView_clicked(self, index):
        self.explr._ui.listView.setCurrentIndex(index)
        uuid = index.data(role=0x0100)
        if uuid:
            logic.load_single_image(uuid)

            ### next highlight the selected item in the list
            ### prolly move to custom_widgets

            for instance in model.public.widget_models["image_list"].instances:
                if instance.origin == "db_explorer":
                    for i in range(instance.widget.model().rowCount()):
                        _uuid = instance.widget.model().index(i, 0).data(role=0x0100)
                        if uuid == _uuid:
                            instance.widget.setCurrentIndex(
                                instance.widget.model().index(i, 0)
                            )
                            break


class Ctrls(QWidget):
    def __init__(self):
        super().__init__()

        self._ui = ctrls_ui()
        self._ui.setupUi(self)

        self._ui.btn_add_image_to_db.clicked.connect(add_images_to_db)
        self._ui.btn_remove_image_from_db.clicked.connect(remove_image_from_db)

        self._ui.btn_add_db.clicked.connect(add_db)
        self._ui.btn_remove_db.clicked.connect(remove_db)
        self._ui.btn_delete_db.clicked.connect(delete_db)

        self._ui.pb_copy_metadata.clicked.connect(copy_metadata)
        self._ui.pb_paste_metadata.clicked.connect(paste_metadata)

        self._ui.btn_write_to_curr_db.clicked.connect(logic.write_to_db)
        self._ui.btn_write_to_new_db.clicked.connect(logic.write_to_new_db)


class Explr(QWidget):
    """User loads files for post-processing."""

    def __init__(self):
        super().__init__()

        self._ui = explr_ui()
        self._ui.setupUi(self)

        self._ui.graphWidget.heightForWidth = lambda arg__1: int(
            2 / 3 * arg__1
        )  # arg__1 is width

        # deactivate wheel event for combobox to prevent accidental changes
        self._ui.cb_img_type.wheelEvent = lambda e: None
        self._ui.cb_drk_group.wheelEvent = lambda e: None
        self._ui.cb_ref_group.wheelEvent = lambda e: None
        self._ui.cb_meas_group.wheelEvent = lambda e: None
        self._ui.cb_wavelength.wheelEvent = lambda e: None
        self._ui.cb_location.wheelEvent = lambda e: None
        self._ui.graphWidget.getView().setMouseMode(pg.ViewBox.PanMode)
        self._ui.graphWidget.getView().setBackgroundColor("#1b1d23")

        # self._ui.treeWidget.dragEnterEvent = self.dragEnterEvent
        # self._ui.treeWidget.dropEvent = self.dropEvent

        self._ui.btn_chang_data_dir.clicked.connect(self.on_data_dir_change)

        self._ui.cb_img_type.activated.connect(self.do_update_current_img_type)
        self._ui.cb_drk_group.activated.connect(self.do_update_current_drk_group)
        self._ui.cb_ref_group.activated.connect(self.do_update_current_ref_group)
        self._ui.cb_meas_group.activated.connect(self.do_update_current_meas_group)
        self._ui.cb_wavelength.activated.connect(self.do_update_wavelength)

        self._ui.le_coords_mm.editingFinished.connect(self.do_update_coords_mm)
        self._ui.dsb_px2mm.editingFinished.connect(self.do_update_px2mm)
        self._ui.cb_location.activated.connect(self.do_update_location)

        self._ui.cb_update_ROIs.stateChanged.connect(self.on_roi_cb_state_changed)
        self._ui.cb_update_coords_pix.stateChanged.connect(
            self.on_coords_pix_cb_state_changed
        )

        self.viewr = Viewr(self._ui.graphWidget)
        self.viewr.redraw = self.redraw
        self.viewr.contextMenuEvent = self.contextMenuEvent

        self.setParametersEnabled(False)

        # model.signals.update_dbs.connect(self.update_dbs)
        model.signals.refresh_db.connect(self.update_view)
        # model.signals.change_img.connect(self.change_img)
        model.signals.focus_list.connect(self.focus_list)
        model.signals.redraw_img.connect(self.redraw)

        self.setParametersEnabled(True)

    def setParametersEnabled(self, _bool):
        self._ui.le_filepath.setEnabled(_bool)
        self._ui.cb_img_type.setEnabled(_bool)
        self._ui.cb_drk_group.setEnabled(_bool)
        self._ui.cb_ref_group.setEnabled(_bool)
        self._ui.cb_meas_group.setEnabled(_bool)
        self._ui.cb_wavelength.setEnabled(_bool)
        self._ui.le_date.setEnabled(_bool)
        self._ui.cb_location.setEnabled(_bool)
        self._ui.le_coords_mm.setEnabled(_bool)
        self._ui.dsb_px2mm.setEnabled(_bool)
        self._ui.le_comment.setEnabled(_bool)

    def on_data_dir_change(self):
        uuid = model.public.raw_image_dbs.current
        print(f"changing data dir {uuid}")

        if uuid is not None:
            current_data_dir = model.public.raw_image_dbs.items[uuid].info["data_dir"]
            new_data_dir = change_data_dir(current_data_dir)
            if new_data_dir:
                self._ui.le_data_directory.setText(new_data_dir)
                logic.change_data_dir(uuid, new_data_dir)

    def do_remove_image_from_db(self):  # OBS ?
        items = self._ui.listWidget.selectedItems()
        uids = []
        for item in items:
            uids.append(item.data(Qt.UserRole))
        logic.remove_images_from_db(uids)

    def get_selected_uuids(self):
        selected = self._ui.listView.selectionModel().selectedRows()
        uuids = []
        for item in selected:
            uuids.append(int(item.data(role=0x0100)))
        return uuids

    def do_update_current_img_type(self, idx):
        val = self._ui.cb_img_type.itemText(idx)
        uuids = self.get_selected_uuids()
        logic.update_img_type(val, uuids)

    def do_update_current_drk_group(self, idx):
        val = self._ui.cb_drk_group.itemText(idx)
        uuids = self.get_selected_uuids()
        logic.update_current_drk_group(val, uuids)

    def do_update_current_ref_group(self, idx):
        val = self._ui.cb_ref_group.itemText(idx)
        uuids = self.get_selected_uuids()
        logic.update_current_ref_group(val, uuids)

    def do_update_current_meas_group(self, idx):
        val = self._ui.cb_meas_group.itemText(idx)
        uuids = self.get_selected_uuids()
        logic.update_current_meas_group(val, uuids)

    def do_update_wavelength(self, idx):
        val = self._ui.cb_wavelength.itemText(idx)
        uuids = self.get_selected_uuids()
        logic.update_wavelength(val, uuids)

    def do_update_coords_mm(self):
        val = self._ui.le_coords_mm.text()
        uuids = self.get_selected_uuids()
        logic.update_coords_mm(val, uuids)

    def do_update_px2mm(self):
        val = self._ui.dsb_px2mm.value()
        uuids = self.get_selected_uuids()
        logic.update_px2mm(val, uuids)

    def do_update_location(self, idx):
        val = self._ui.cb_location.itemText(idx)
        uuids = self.get_selected_uuids()
        logic.update_location(val, uuids)

    def do_paste_metadata(self):
        selected = self._ui.listWidget.selectedItems()

        uids = []
        for item in selected:
            uids.append(int(item.data(Qt.UserRole)))

        logic.paste_metadata(uids)

    def on_roi_cb_state_changed(self):
        state = self._ui.cb_update_ROIs.checkState()
        if state == Qt.CheckState.Checked:
            self.toggle_rois_movable(True)
        elif state == Qt.CheckState.PartiallyChecked:
            self.toggle_rois_visible(True)
        else:
            self.toggle_rois_movable(False)
            self.toggle_rois_visible(False)

        self.focus_list()

    def on_coords_pix_cb_state_changed(self):
        state = self._ui.cb_update_coords_pix.checkState()
        if state == Qt.CheckState.Checked:
            self.toggle_coords_pix_movable(True)
        elif state == Qt.CheckState.PartiallyChecked:
            self.toggle_coords_pix_visible(True)
        else:  # unchecked
            self.toggle_coords_pix_movable(False)
            self.toggle_coords_pix_visible(False)

        self.focus_list()

    def focus_list(self):
        uuid = model.private["current_img_uuid"]

        for instance in model.public.widget_models["image_list"].instances:
            if instance.origin == "db_explorer":
                for i in range(instance.widget.model().rowCount()):
                    idx = instance.widget.model().index(i, 0)
                    if instance.widget.model().data(idx, role=0x0100) == uuid:
                        instance.widget.setCurrentIndex(idx)
                        break

        self._ui.listView.setFocus()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        action_addROI_white = menu.addAction("Add white ROI")
        action_addROI_gray = menu.addAction("Add gray ROI")
        action_removeROI_white = menu.addAction("Remove white ROI")
        action_removeROI_gray = menu.addAction("Remove gray ROI")
        menu.addSeparator()
        action_removeROI_all = menu.addAction("Remove all ROIs")
        action_addROI_ref = menu.addAction("Add reference ROI")

        uuids = self.get_selected_uuids()

        res = menu.exec_(event.globalPos())
        if res == action_addROI_white:
            logic.add_ROI(uuids, "white")
        elif res == action_addROI_gray:
            logic.add_ROI(uuids, "gray")
        elif res == action_removeROI_white:
            logic.remove_ROI(uuids, "white")
        elif res == action_removeROI_gray:
            logic.remove_ROI(uuids, "gray")
        elif res == action_removeROI_all:
            logic.remove_ROI(uuids, "all")
        elif res == action_addROI_ref:
            logic.add_ROI(uuids, "ref")

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
        else:
            super(QTreeWidget, self._ui.treeWidget).dragEnterEvent(e)

    # TODO: [!] Rework drag drop stuff such that it doesn't drop into another level
    def dragMoveEvent(self, e):
        self._ui.treeWidget.setDropIndicatorShown(True)
        super(QTreeWidget, self._ui.treeWidget).dragMoveEvent(e)
        if self._ui.treeWidget.dropIndicatorPosition() == QTreeWidget.OnItem:
            self._ui.treeWidget.setDropIndicatorShown(False)
            e.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            files = []
            for url in event.mimeData().urls():
                path_to_file = url.path()[1:]
                if path_to_file.endswith("py"):
                    files.append(path_to_file)

                else:
                    print("Not a python file")
                self.add_images(files)
                event.acceptProposedAction()
        else:
            super(QTreeWidget, self._ui.treeWidget).dropEvent(event)

    def add_images(self, files):
        print(files)

    def update_view(self):
        database = model.public.img_set

        self._ui.cb_img_type.clear()
        self._ui.cb_drk_group.clear()
        self._ui.cb_ref_group.clear()
        self._ui.cb_meas_group.clear()
        self._ui.cb_wavelength.clear()
        self._ui.cb_location.clear()
        self._ui.dsb_px2mm.clear()

        print(
            f"RUNNING: update_view in db_explorer (view) for {len(database._image_db)} images"
        )

        uuid = model.public.raw_image_dbs.current
        if uuid is not None:
            self._ui.le_data_directory.setText(
                model.public.raw_image_dbs.items[uuid].info["data_dir"]
            )

        for i, item in enumerate(database._image_db.items()):
            id, entry = item

            # TODO: set alternating background color for each set of images

            _item = QTreeWidgetItem(
                [str(id), str(entry.ID), str(entry.filepath).split("/")[-1]]
            )
            _item.setFlags(_item.flags() & ~Qt.ItemIsDropEnabled)

            _item = QListWidgetItem()
            _string = f"{str(entry.filepath).split('/')[-1]}"
            _string = f"{'filename: ' + _string: <80} (id: {entry.ID})"
            _item.setText(_string)
            _item.setData(Qt.ItemDataRole.UserRole, id)
            # self._ui.listWidget.addItem(_item)

            # populate from database
            if str(entry.img_type) not in [
                self._ui.cb_img_type.itemText(i)
                for i in range(self._ui.cb_img_type.count())
            ]:
                self._ui.cb_img_type.addItem(str(entry.img_type))

            if str(entry.drk_group) not in [
                self._ui.cb_drk_group.itemText(i)
                for i in range(self._ui.cb_drk_group.count())
            ]:
                # self._ui.cb_drk_group.addItem(str(entry.drk_group))
                self._ui.cb_drk_group.insertItem(
                    entry.drk_group, str(entry.drk_group)
                )  # only works for increasing integers, better to post-sort?

            if str(entry.ref_group) not in [
                self._ui.cb_ref_group.itemText(i)
                for i in range(self._ui.cb_ref_group.count())
            ]:
                # self._ui.cb_ref_group.addItem(str(entry.ref_group))
                self._ui.cb_ref_group.insertItem(
                    entry.ref_group, str(entry.ref_group)
                )  # only works for increasing integers

            if str(entry.meas_group) not in [
                self._ui.cb_meas_group.itemText(i)
                for i in range(self._ui.cb_meas_group.count())
            ]:
                self._ui.cb_meas_group.addItem(str(entry.meas_group))

            if str(entry.wavelength) not in [
                self._ui.cb_wavelength.itemText(i)
                for i in range(self._ui.cb_wavelength.count())
            ]:
                self._ui.cb_wavelength.addItem(str(entry.wavelength))

            if str(entry.location) not in [
                self._ui.cb_location.itemText(i)
                for i in range(self._ui.cb_location.count())
            ]:
                self._ui.cb_location.addItem(str(entry.location))

        self.redraw()

    def redraw(self):
        db_entry = model.private["current_db_entry"]
        curr_img = model.private["current_img"]

        self.show_selected(curr_img, db_entry, redraw=True)

    def show_selected(self, img, db_entry, redraw=False):
        # self.current_entry = db_entry  # FIXME: This should be handled in the plugin

        self.clean_rois()

        if db_entry is not None:  # if None then no image is selected
            if not isinstance(img._data, FileNotFoundError):
                if not redraw:
                    self.viewr.imv.setImage(img._data.T)
                    self.viewr.imv.getRoiPlot().hide()  ## TODO: Remove roiPlot from viewr instead

                self._ui.le_filepath.setText(str(db_entry.filepath))

                self._ui.le_date.setText(str(db_entry.date))

                index = self._ui.cb_img_type.findText(str(db_entry.img_type))
                self._ui.cb_img_type.setCurrentIndex(index)

                index = self._ui.cb_drk_group.findText(str(db_entry.drk_group))
                self._ui.cb_drk_group.setCurrentIndex(index)

                index = self._ui.cb_ref_group.findText(str(db_entry.ref_group))
                self._ui.cb_ref_group.setCurrentIndex(index)

                index = self._ui.cb_meas_group.findText(str(db_entry.meas_group))
                self._ui.cb_meas_group.setCurrentIndex(index)

                index = self._ui.cb_wavelength.findText(str(db_entry.wavelength))
                self._ui.cb_wavelength.setCurrentIndex(index)

                index = self._ui.cb_location.findText(str(db_entry.location))
                self._ui.cb_location.setCurrentIndex(index)

                self._ui.le_coords_mm.setText(str(db_entry.coords_mm))
                self._ui.le_coords_pix.setText(str(db_entry.coords_pix))

                self._ui.dsb_px2mm.setValue(db_entry.px_2_mm)

                self._ui.le_comment.setText(str(db_entry.comment))

                self.add_coords_pix(db_entry.coords_pix, img)

                self.add_ROIs(db_entry.ROI, img)

            else:
                _img = np.zeros((200, 300))
                putText(
                    _img,
                    "File not found",
                    (40, 110),
                    0,
                    1,
                    (255, 255, 255),
                    2,
                    1,
                    False,
                )
                self._ui.graphWidget.setImage(_img.T[:, ::1])

    def add_coords_pix(self, coords, img, color="g"):
        img_size = pro.get_img_size(img)

        point_px = [coords[0] * img_size[0], coords[1] * img_size[1]]

        point_handle = pg.TargetItem(
            point_px,
            size=15,
            pen=pg.mkPen(color, width=1),
            brush=(255, 255, 255, 0),
            hoverPen=pg.mkPen(color, width=2),
            hoverBrush=(255, 255, 255, 0),
        )

        state = self._ui.cb_update_coords_pix.checkState()
        if state == Qt.CheckState.Checked:
            point_handle.movable = True
            point_handle.setVisible(True)
        elif state == Qt.CheckState.PartiallyChecked:
            point_handle.movable = False
            point_handle.setVisible(True)
        else:  # unchecked
            point_handle.movable = False
            point_handle.setVisible(False)

        point_handle.sigPositionChangeFinished.connect(
            lambda val, img=img: self.do_update_coords_pix(val, img)
        )

        self._ui.graphWidget.addItem(point_handle)
        self.coords_pix_handle = point_handle

    def add_ROIs(self, ROI, img, color="r"):
        img_size = pro.get_img_size(img)
        colors = ["g", "r"]  # green for gray targets and red for white

        ROI_handles = []
        TEXT_handles = []

        for i, roi in enumerate(ROI):
            color = colors[i]

            roi_handles = []
            text_handles = []

            for j in range(len(roi)):
                pos, size = pro.ROI_pos_to_size(roi[j], img_size)
                roi_handle = pg.RectROI(pos, size, pen=(color))

                state = self._ui.cb_update_ROIs.checkState()
                if state == Qt.CheckState.Checked:
                    roi_handle.translatable = True
                    roi_handle.resizable = True
                    roi_handle.getHandles()[0].show()
                    roi_handle.setVisible(True)
                elif state == Qt.CheckState.PartiallyChecked:
                    roi_handle.translatable = False
                    roi_handle.resizable = False
                    roi_handle.getHandles()[0].hide()
                    roi_handle.setVisible(True)
                else:  # unchecked
                    roi_handle.translatable = False
                    roi_handle.setVisible(False)

                roi_handle.sigRegionChangeFinished.connect(
                    lambda roi,
                    handle=roi_handle,
                    img=img,
                    idx=(i, j): self.do_update_roi(roi, handle, img, idx)
                )

                roi_handles.append(roi_handle)
                self._ui.graphWidget.addItem(roi_handle)

                # avs = pro.average_in_ROI(self.current_img._data, [roi[j]])[0]
                avs = pro.average_in_ROI(model.private["current_img"]._data, [roi[j]])[
                    0
                ]

                text = pg.TextItem(
                    ", ".join(str(round(av, 3)) for av in avs),
                    color="k",
                    fill=pg.mkBrush((255, 255, 255, 175)),
                    ensureInBounds=True,
                )

                self._ui.graphWidget.addItem(text)
                text.setPos(pos[0] + size[0], pos[1])
                text_handles.append(text)
                if (
                    state == Qt.CheckState.Checked
                    or state == Qt.CheckState.PartiallyChecked
                ):
                    text.setVisible(True)
                else:
                    text.setVisible(False)

            ROI_handles.append(roi_handles)
            TEXT_handles.append(text_handles)

        self.ROI_handles = ROI_handles
        self.TEXT_handles = TEXT_handles

    def toggle_rois_movable(self, state):
        if hasattr(self, "ROI_handles"):
            for roi_handles in self.ROI_handles:
                for roi_handle in roi_handles:
                    roi_handle.translatable = state
                    roi_handle.resizable = state

                    # show handles
                    for handle in roi_handle.getHandles():
                        handle.setVisible(True)

        self._ui.graphWidget.update() # FIX: Zoom issue after toggle ROI

    def toggle_rois_visible(self, state):
        if hasattr(self, "ROI_handles"):
            for roi_handles, text_handles in zip(self.ROI_handles, self.TEXT_handles):
                for roi_handle, text_handle in zip(roi_handles, text_handles):
                    roi_handle.setVisible(state)
                    text_handle.setVisible(state)

                    # hide handles BUG reappears when clicking ROI
                    for handle in roi_handle.getHandles():
                        handle.setVisible(False)



    def toggle_coords_pix_movable(self, state):
        if hasattr(self, "coords_pix_handle"):
            self.coords_pix_handle.movable = state

    def toggle_coords_pix_visible(self, state):
        if hasattr(self, "coords_pix_handle"):
            self.coords_pix_handle.setVisible(state)

    def clean_rois(self):
        if hasattr(self, "ROI_handles"):
            for roi_handles in self.ROI_handles:
                for roi_handle in roi_handles:
                    self._ui.graphWidget.removeItem(roi_handle)

        if hasattr(self, "TEXT_handles"):
            for text_handles in self.TEXT_handles:
                for text_handle in text_handles:
                    self._ui.graphWidget.removeItem(text_handle)

        if hasattr(self, "coords_pix_handle"):
            self._ui.graphWidget.removeItem(self.coords_pix_handle)

    def do_update_coords_pix(self, val, img):
        img_size = pro.get_img_size(img)

        print("Updating coords_pix")
        # self.current_entry.coords_pix
        val = str([round(px / img_size[i], 5) for i, px in enumerate(list(val.pos()))])
        logic.update_coords_pix(val)
        self._ui.le_coords_pix.setText(val)

        # plugins.redraw_viewr(self.viewr)

    # TODO: move to parent if used identically in multiple views
    def do_update_roi(self, roi, handle, img, idx):
        print("Updating roi")

        img_size = pro.get_img_size(img)

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

        logic.update_ROI(idx, [[x0, y0], [x1, y1]])

        self.TEXT_handles[idx[0]][idx[1]].setPos(
            roi.pos().x() + roi.size().x(), roi.pos().y()
        )

        avs = pro.average_in_ROI(img._data, [[[x0, y0], [x1, y1]]])[0]
        self.TEXT_handles[idx[0]][idx[1]].setText(
            ", ".join(str(round(av, 3)) for av in avs)
        )


view = View()


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        pass

    def initialize(self):
        super().__init__(None)
        self.setWindowTitle("Settings")

        layout = QVBoxLayout()

        self.checkboxes = []

        # Add checkboxes for settings
        self.checkboxes.append(QCheckBox("SELECT ALL"))
        layout.addWidget(self.checkboxes[0])

        self.checkboxes.append(QCheckBox("ROI"))
        layout.addWidget(self.checkboxes[1])

        self.checkboxes.append(QCheckBox("img_type"))
        layout.addWidget(self.checkboxes[2])

        self.checkboxes.append(QCheckBox("drk_group"))
        layout.addWidget(self.checkboxes[3])

        self.checkboxes.append(QCheckBox("ref_group"))
        layout.addWidget(self.checkboxes[4])

        self.checkboxes.append(QCheckBox("meas_group"))
        layout.addWidget(self.checkboxes[5])

        self.checkboxes.append(QCheckBox("wavelength"))
        layout.addWidget(self.checkboxes[6])

        self.checkboxes.append(QCheckBox("location"))
        layout.addWidget(self.checkboxes[7])

        self.checkboxes.append(QCheckBox("coords_mm"))
        layout.addWidget(self.checkboxes[8])

        self.checkboxes.append(QCheckBox("coords_pix"))
        layout.addWidget(self.checkboxes[9])

        self.checkboxes.append(QCheckBox("px_2_mm"))
        layout.addWidget(self.checkboxes[10])

        self.checkboxes.append(QCheckBox("comment"))
        layout.addWidget(self.checkboxes[11])

        # Add accept button
        accept_button = QPushButton("Accept")
        accept_button.clicked.connect(self.accept_settings)
        layout.addWidget(accept_button)

        self.setLayout(layout)

    def accept_settings(self):
        selected_settings = []

        # Get selected settings
        if self.checkboxes[0].isChecked():  # select all
            selected_settings = [checkbox.text() for checkbox in self.checkboxes[1:]]
        else:
            for checkbox in self.checkboxes:
                if checkbox.isChecked():
                    selected_settings.append(checkbox.text())

        # Call the function in the plugin to handle the selected settings
        logic.copy_metadata(selected_settings)

        self.accept()


settings_dialog = SettingsDialog()
