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

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow

from snowimagerpro.app.managers import plugins
from snowimagerpro.app.managers.settings import user_config
from snowimagerpro.app.plugins.base import public_data
from snowimagerpro.app.ui.main_window_ui import Ui_MainWindow

logger = "main_view"


class MainView(QMainWindow):
    def __init__(self, title: str, icon_path: str, theme_path: str):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(icon_path))

        with open(theme_path, "r") as f:
            self.setStyleSheet(f.read())

        # Add plugins to UI and connect signals
        for name, model, view, logic in plugins.plugins:
            logging.getLogger(logger).info(
                f"Adding '{name}' to UI and connecting private signals."
            )

            self.ui.toolBox.addTab(view.ctrls, QIcon(view._icon), "")
            self.ui.stackedWidget.addWidget(view.explr)

            # REMOVE: should be able to set directly from shared data ...
            # model.public.img_set.sig_progress.connect(self.ui.progress_bar.setValue)
            # model.public.img_set.sig_status.connect(self.ui.status_message.setText)

            # TODO: connect signals from private models to UI
            # model.private...

        # Connect shared data (public) signals
        logging.getLogger(logger).info("Connecting public signals to UI.")
        public_data.img_set.sig_progress.connect(self.update_progress_bar)
        public_data.img_set.sig_status.connect(self.ui.status_message.setText)
        # TODO: dont go down to img_set, but connect to public_data directly and connect to img_set in to model

        self.ui.toolBox.currentChanged.connect(self.ui.stackedWidget.setCurrentIndex)
        self.ui.toolBox.setCurrentIndex(user_config.get("initial_tab") or 0)

    def update_progress_bar(self, value):
        print(f"Setting progress bar to {value}")
        if value >= 0:
            if not self.ui.progress_bar.isTextVisible():
                self.ui.progress_bar.setTextVisible(True)
            self.ui.progress_bar.setValue(value)
        else:
            self.ui.progress_bar.setValue(0)
            self.ui.progress_bar.setTextVisible(False)

    def closeEvent(self, event):
        # Close views in plugins, save user config and close UI
        for name, model, view, logic in plugins.plugins:
            if len(logic.views) > 0:
                logging.getLogger(logger).info(f"Closing views in {name}:")
                logic.close_views()

        # Save user config
        user_config.set("initial_tab", self.ui.toolBox.currentIndex())
        user_config.save()

        super().closeEvent(event)
        logging.getLogger(logger).info("Closing UI.")
