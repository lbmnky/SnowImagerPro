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
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem, QMenu, QWidget, QFileDialog

from snowimagerpro.app.managers import user_config
from snowimagerpro.app.managers.paths import paths
from snowimagerpro.app.plugins.base import ViewBase

from .logic import logic
from .model import model
from .ui.ctrls_ui import Ui_Form as ctrls_ui
from .ui.explr_ui import Ui_Form as explr_ui
from .viewr import getOpenFileName, show_warning, getSaveFileNameMod, yes_no_warning


class View(ViewBase):
    def __init__(self):
        super(View, self).__init__()
        self._name = "image processor"

    def do_update(self):
        print("RUNNING: do_update in image_processor (view)")
        model.public.widget_models["image_tree"].refresh()

    def initialize(self):
        self.ctrls = Ctrls()
        self.explr = Explr()

        self._icon = paths.resource("icons/processing.svg")

        logic.update_view.connect(self.explr.do_update)

        # self.explr._ui.comboBox.setModel(db_model.combo_if)
        # self.explr._ui.comboBox.activated.connect(db_model.change_selected)
        # db_model.combo_if.instances.append(self.explr._ui.comboBox)

        model.public.sync_widget_to_model(
            self.explr._ui.comboBox, "db_combo", "image_processor"
        )
        model.public.sync_widget_to_model(
            self.explr._ui.treeView, "image_tree", "image_processor"
        )
        model.public.sync_widget_to_model(
            self.explr._ui.comboBox_2, "sortby_list", "image_processor"
        )

        model.public.raw_image_dbs._update.connect(self.do_update)

    def post_init(self):
        print("post_init IS implemnted for image_processor (view)")

        for instance in model.public.widget_models["image_tree"].instances:
            if instance.origin == "image_processor":
                instance.widget.selectionModel().selectionChanged.connect(
                    self.explr.on_select_images
                )


class Ctrls(QWidget):
    def __init__(self):
        super().__init__()

        self._ui = ctrls_ui()
        self._ui.setupUi(self)

        self._ui.btn_load.clicked.connect(logic.load)

        self._ui.btn_preview.clicked.connect(self.on_btn_preview_clicked)

        self._ui.btn_ffc.clicked.connect(logic.ffc)
        self._ui.btn_ffc.setContextMenuPolicy(Qt.CustomContextMenu)
        self._ui.btn_ffc.customContextMenuRequested.connect(self.ffc_context_menu)

        self._ui.btn_refl_calib.clicked.connect(logic.refl_cal)
        self._ui.btn_refl_calib.setContextMenuPolicy(Qt.CustomContextMenu)
        self._ui.btn_refl_calib.customContextMenuRequested.connect(
            self.refl_context_menu
        )

        self._ui.btn_show_processed.clicked.connect(logic.show_processed)

        self._ui.btn_undistort_images.clicked.connect(logic.undistort_images)
        self._ui.btn_undistort_images.setContextMenuPolicy(Qt.CustomContextMenu)
        self._ui.btn_undistort_images.customContextMenuRequested.connect(
            self.undistort_context_menu
        )

        self._ui.sb_overlap_x.valueChanged.connect(logic.update_overlap_x)
        self._ui.sb_overlap_y.valueChanged.connect(logic.update_overlap_y)

        self._ui.sb_overlap_x.setValue(user_config.get("processor.overlap_x"))
        self._ui.sb_overlap_y.setValue(user_config.get("processor.overlap_y"))

        self._ui.btn_stitch.clicked.connect(logic.stitch_images)

        self._ui.btn_save.clicked.connect(self.on_btn_save_clicked)

        self._ui.btn_debug.clicked.connect(logic.toggle_debug)

        self._ui.btn_close_views.clicked.connect(logic.close_views)

    def ffc_context_menu(self, pos):
        if hasattr(model.public.img_set, "imgs_post_ffc"):
            menu = QMenu()
            action = menu.addAction("Remove flat-field correction")
            action.triggered.connect(logic.remove_ffc)
            menu.exec_(self._ui.btn_ffc.mapToGlobal(pos))

    def refl_context_menu(self, pos):
        if hasattr(model.public.img_set, "imgs_post_refl_cal"):
            menu = QMenu()
            action = menu.addAction("Remove reflectance correction")
            action.triggered.connect(logic.remove_refl)
            menu.exec_(self._ui.btn_refl_calib.mapToGlobal(pos))

    def undistort_context_menu(self, pos):
        if hasattr(model.public.img_set, "imgs_post_undistort"):
            menu = QMenu()
            action = menu.addAction("Remove undistortion")
            action.triggered.connect(logic.remove_undistort)
            menu.exec_(self._ui.btn_undistort_images.mapToGlobal(pos))

    def on_btn_preview_clicked(self):
        show_dark = self._ui.cb_preview_dark.isChecked()
        show_ref = self._ui.cb_preview_ref.isChecked()

        logic.show_raw(show_dark=show_dark, show_ref=show_ref)

    def on_btn_save_clicked(self):
        if hasattr(model.public.img_set, "stitched_image"):

            dtime = datetime.now().strftime("%Y%m%d_%H%M")
            date = model.public.img_set.stitched_image["ngr"]._meta["date"]
            location = model.public.img_set.stitched_image["ngr"]._meta["location"]


            h5_path = user_config.get("processor.h5_path")

            if Path(h5_path).exists():
                fn = Path(h5_path) / Path(f"{date}_{location}") / Path(f"processedOn_{dtime}.h5") # TODO: how to write path/filename.ext into the input field of QFileDialog?
                #fn = Path(h5_path) / Path(f"processedOn_{dtime}.h5")
            else:
                fn = Path("~/processedOn_{dtime}.h5").expanduser()

            folder = fn.parent
            #if not folder.exists():
            #    folder.mkdir(parents=True)
            #    dir_created = True
            #else:
            #    dir_created = False

            print(folder)
            print(type(folder))


            if folder.exists():
                fp = getSaveFileNameMod(None, "Save File", str(fn), "Image Files (*.h5)")
            else:
                custom_file_name = f"{date}_{location}/processedOn_{dtime}.h5"
                fp = getSaveFileNameMod(None, "Save File", h5_path, "Image Files (*.h5)", custom_file_name=custom_file_name)

            if fp is None:
                return

            fp = Path(fp)
            folder = fp.parent


            logic.save(fp=fp, folder=folder)

        else:
            show_warning(None, "Error", "No stitched image available")


class Explr(QWidget):
    def __init__(self):
        super().__init__()

        self._ui = explr_ui()
        self._ui.setupUi(self)

        self._ui.treeView.activated.connect(self.on_treeView_doubleClicked)

        self._ui.listWidget_nogrid_images.itemSelectionChanged.connect(
            self.on_listWidget_nogrid_itemSelected
        )
        self._ui.listWidget_grid_images.itemSelectionChanged.connect(
            self.on_listWidget_grid_itemSelected
        )
        self._ui.listWidget_ref_images.itemSelectionChanged.connect(
            self.on_listWidget_ref_itemSelected
        )

        self._ui.listWidget_nogrid_images.focusInEvent = (
            self.listWidget_nogrid_focusInEvent
        )
        self._ui.listWidget_grid_images.focusInEvent = self.listWidget_grid_focusInEvent
        self._ui.listWidget_ref_images.focusInEvent = self.listWidget_ref_focusInEvent

        # on double click show image
        #self._ui.listWidget_nogrid_images.itemDoubleClicked.connect(
        #    self.on_listWidget_itemDoubleClicked
        #)
        #self._ui.listWidget_grid_images.itemDoubleClicked.connect(
        #    self.on_listWidget_itemDoubleClicked
        #)
        #self._ui.listWidget_ref_images.itemDoubleClicked.connect(
        #    self.on_listWidget_itemDoubleClicked
        #)

        # on enter and doubleclick show image
        self._ui.listWidget_nogrid_images.activated.connect(
            self.on_listWidget_itemDoubleClicked
        )
        self._ui.listWidget_grid_images.activated.connect(
            self.on_listWidget_itemDoubleClicked
        )
        self._ui.listWidget_ref_images.activated.connect(
            self.on_listWidget_itemDoubleClicked
        )

    def on_treeView_doubleClicked(self, index):
        model.public.select_images_on_doubleclick(index)
        logic.load()

    def listWidget_nogrid_focusInEvent(self, event):
        self._ui.listWidget_nogrid_images.setFocus()
        if self._ui.listWidget_nogrid_images.count() == 0:
            return
        try:
            item = self._ui.listWidget_nogrid_images.selectedItems()[0]
            uuid = item.data(Qt.ItemDataRole.UserRole)
            # self._ui.listWidget_nogrid_images.setCurrentRow(item.row())
        except IndexError:
            uuid = self._ui.listWidget_nogrid_images.item(0).data(
                Qt.ItemDataRole.UserRole
            )
            self._ui.listWidget_nogrid_images.setCurrentRow(0)

        super().focusInEvent(event)
        self.show_meta(uuid)

    def listWidget_grid_focusInEvent(self, event):
        self._ui.listWidget_grid_images.setFocus()
        if self._ui.listWidget_grid_images.count() == 0:
            return
        try:
            uuid = self._ui.listWidget_grid_images.selectedItems()[0].data(
                Qt.ItemDataRole.UserRole
            )
        except IndexError:
            uuid = self._ui.listWidget_grid_images.item(0).data(
                Qt.ItemDataRole.UserRole
            )
            self._ui.listWidget_grid_images.setCurrentRow(0)

        super().focusInEvent(event)
        self.show_meta(uuid)

    def listWidget_ref_focusInEvent(self, event):
        self._ui.listWidget_ref_images.setFocus()
        if self._ui.listWidget_ref_images.count() == 0:
            return
        try:
            uuid = self._ui.listWidget_ref_images.selectedItems()[0].data(
                Qt.ItemDataRole.UserRole
            )
        except IndexError:
            uuid = self._ui.listWidget_ref_images.item(0).data(Qt.ItemDataRole.UserRole)
            self._ui.listWidget_ref_images.setCurrentRow(0)

        super().focusInEvent(event)
        self.show_meta(uuid)

    def on_select_images(self, selected, deselected):
        indices = self._ui.treeView.selectionModel().selectedIndexes()
        model.public.select_images(indices)
        if len(indices) == 1:
            uuid = indices[0].data(role=0x0100)
            if uuid is not None:
                self.show_meta(int(uuid))

    def on_listWidget_nogrid_itemSelected(self):
        selected = self._ui.listWidget_nogrid_images.selectedItems()[0]
        uuid = selected.data(Qt.ItemDataRole.UserRole)
        self.show_meta(uuid)

    def on_listWidget_grid_itemSelected(self):
        selected = self._ui.listWidget_grid_images.selectedItems()[0]
        uuid = selected.data(Qt.ItemDataRole.UserRole)
        self.show_meta(uuid)

    def on_listWidget_ref_itemSelected(self):
        selected = self._ui.listWidget_ref_images.selectedItems()[0]
        uuid = selected.data(Qt.ItemDataRole.UserRole)
        self.show_meta(uuid)

    def show_meta(self, uuid):
        db_entry = model.public.img_set._image_db[uuid]

        text = (
            f"Filepath: {db_entry.filepath}\n"
            f"UUID: {db_entry.ID}\n"
            f"Wavelength: {db_entry.wavelength}\n"
            f"Dark group: {db_entry.drk_group}\n"
            f"Ref group: {db_entry.ref_group}\n"
            f"Location: {db_entry.location}\n"
            f"Date: {db_entry.date}\n"
            f"Comment: {db_entry.comment}"
        )

        self._ui.show_meta.setText(text)
        self.show_exif(uuid)

    def show_exif(self, uuid):
        exif = model.public.img_set._image_db[uuid].exif

        text = (
            f"Type: {exif['Image ImageDescription']}\n"
            f"Author: {exif['Image Make']}\n"
            f"Exposure time: {exif['Image ExposureTime']}\n"
            f"Iso: {exif['Image ISOSpeedRatings']}\n"
            f"Date: {exif['Image DateTimeOriginal']}\n"
            f"Serial number: {exif['Image BodySerialNumber']}\n"
            f"Black Level: {exif['Image BlackLevel']}\n"
            f"Width: {exif['Image ImageWidth']}, Length {exif['Image ImageLength']}\n"
            f"Bits per sample: {exif['Image BitsPerSample']}\n"
        )
        self._ui.show_exif.setText(text)


    def on_listWidget_itemDoubleClicked(self, item):
        uuid = item.data(Qt.ItemDataRole.UserRole)
        logic.show_raw(uuid)

    def do_update(self):
        print("RUNNING: do_update_2 in image_processor (view/explr)")

        self._ui.listWidget_nogrid_images.clear()
        self._ui.listWidget_grid_images.clear()
        self._ui.listWidget_ref_images.clear()

        for uuid in model.public.img_set._selected_images:
            img = model.public.img_set._image_db[uuid]
            item = QListWidgetItem(img.filepath.name)
            item.setData(Qt.ItemDataRole.UserRole, uuid)

            if img.img_type == "ngr":
                self._ui.listWidget_nogrid_images.addItem(item)
            elif img.img_type == "gri":
                self._ui.listWidget_grid_images.addItem(item)
            elif img.img_type == "ref":
                self._ui.listWidget_ref_images.addItem(item)


view = View()
