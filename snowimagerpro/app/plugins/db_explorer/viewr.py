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

from ..base import (
    ViewrBase,
    getFileName,
    getOpenFileName,
    getSaveFileName,
    show_warning,
    yes_no_warning,
)

__all__ = [
    "Viewr",
    "getOpenFileName",
    "getSaveFileName",
    "show_warning",
    "getFileName",
    "yes_no_warning",
]


class Viewr(ViewrBase):
    # TODO: Implement the view for the db_explorer plugin. It mixes with Explr ...

    def __init__(self, widget, parent=None):
        super().__init__(parent)
        self.imv = widget

        self.imv.ui.roiBtn.hide()
        self.imv.ui.menuBtn.hide()
        self.imv.ui.histogram.setBackground("#1b1d23")
        self.imv.ui.roiPlot.setEnabled(False)
        self.imv.ui.roiPlot.setFixedHeight(0)
        self.imv.ui.roiPlot.setFrameStyle(0)
        self.imv.ui.roiPlot.setUpdatesEnabled(False)
        self.imv.ui.roiPlot.hide()

    def show(self, data):
        super(ViewrBase).show()
