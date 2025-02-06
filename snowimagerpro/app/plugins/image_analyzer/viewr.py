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

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QSplitter

from ..base import ViewrBase, getOpenFileName, getSaveFileName, show_warning

__all__ = ["Viewr", "getOpenFileName", "getSaveFileName", "show_warning"]


class Viewr(ViewrBase):
    region_changed = Signal(tuple)

    def __init__(self):
        super().__init__(parent=None)
        splitter = QSplitter(self)
        h_layout = QHBoxLayout()
        h_layout.addWidget(splitter)

        self.setLayout(h_layout)
        self.h_layout = h_layout
        self.splitter = splitter

    def show(self, data):
        if isinstance(data, np.ndarray) or isinstance(data, list):
            plts = []
            if len(np.shape(data)) == 2:
                plt = self.show_img(data)
                plts.append(plt)
            elif len(np.shape(data)) == 1:
                plt = self.show_profile(data)
                plts.append(plt)
            else:
                print("not showing")

        elif isinstance(data, dict):
            plts = []
            for key, value in data.items():
                if len(np.shape(value)) == 2:
                    plt = self.show_img(value, show_hist=False)
                    plt.setTitle(key)
                    if key == "SSA_image":
                        roi = pg.LinearRegionItem(
                            values=[100, 200],
                            orientation="vertical",
                        )
                        roi.sigRegionChangeFinished.connect(
                            lambda reg=roi.getRegion(): self.region_changed.emit(reg)
                        )
                        self.roi = roi
                        plt.addItem(roi)
                    plts.append(plt)
                elif len(np.shape(value)) == 1:
                    plt = self.show_profile(value)
                    plt.setTitle(key)
                    plt.setMouseEnabled(x=False, y=True)
                    plts.append(plt)
                else:
                    print("not showing")

            for plt in plts[1:]:
                plt.setYLink(plts[0])

        self.resize(800, 600)

        super(Viewr, self).show()

    def show_img(self, data, show_hist=True):
        print("showing image")
        plt = pg.PlotItem()
        imv = pg.ImageView(view=plt)
        plt.getViewBox().invertY(False)
        #plt.hideAxis("left")
        plt.hideAxis("bottom")
        data[data==0] = float("nan")
        imv.setImage(data.T[:,::-1])
        self.splitter.addWidget(imv)
        if not show_hist:
            imv.ui.histogram.hide()
            imv.ui.roiBtn.hide()
            imv.ui.menuBtn.hide()
        #imv.adjustSize()
        return plt

    def show_profile(self, data):
        plt = pg.PlotWidget()
        plt.plot(data[::-1], range(len(data)))
        #plt.getViewBox().invertY(True)
        self.splitter.addWidget(plt)
        return plt
