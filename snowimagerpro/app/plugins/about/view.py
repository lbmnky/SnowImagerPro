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

from PySide6.QtWidgets import QTextEdit, QWidget

from snowimagerpro.app.managers.paths import paths

from ..base import ViewBase
from .logic import logic
from .model import model
from .ui.ctrls_ui import Ui_Form as ctrls_ui
from .ui.explr_ui import Ui_Form as explr_ui


class View(ViewBase):
    def __init__(self):
        super(View, self).__init__()
        self._name = "About"

    def initialize(self):
        self.ctrls = Ctrls()
        self.explr = Explr()

        self._icon = paths.resource("icons/about.svg")


class Ctrls(QWidget):
    def __init__(self):
        super().__init__()

        self._ui = ctrls_ui()
        self._ui.setupUi(self)

        self._ui.btn_show_licensing_info.clicked.connect(
            lambda state, info="license": logic.change_text(info)
        )
        self._ui.btn_show_contact_details.clicked.connect(
            lambda state, info="contact": logic.change_text(info)
        )


class Explr(QWidget):
    def __init__(self):
        super().__init__()

        self._ui = explr_ui()
        self._ui.setupUi(self)

        # self._ui.textBrowser.setMaximumWidth(1000)

        model.signals.update_text.connect(self.change_text)

    def change_text(self, info):
        if info == "license":
            with open(paths.resource("about/ThirdPartyNotices.txt"), "r") as f:
                text = f.read()
                self._ui.textBrowser.setFontFamily("monospace")
                self._ui.textBrowser.setFontPointSize(7.8)
                self._ui.textBrowser.setLineWrapMode(QTextEdit.NoWrap)
                self._ui.textBrowser.setPlainText(text)

        if info == "contact":
            self._ui.textBrowser.setLineWrapMode(QTextEdit.WidgetWidth)
            self._ui.textBrowser.setFontPointSize(12)
            self._ui.textBrowser.setHtml("""
                <html>
                <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
                    <div style="text-align: center; margin: auto;">
                        <br>
                        <h2>Contact Information</h2>
                        <p>Email: info@snowimager.com</p>
                        <br>
                        <h2>Visit our website</h2>
                        <p>
                            <a href="https://www.snowimager.com" target="_blank">www.snowimager.com</a>
                        </p>
                        <br>
                        <h2>Follow us on social media</h2>
                        ...
                        <br>
                        <h2>License</h2>
                        <p>This software is licensed under the GNU General Public License. For more details, please refer to the LICENSE file included with this project.</p>
                    </div>
                </body>
                </html>
            """)


view = View()
