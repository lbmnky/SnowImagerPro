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
from io import BytesIO
from pathlib import Path
from typing import List, Union

import numpy as np

# from odscharts.spreadsheet import SpreadSheet
import pyqtgraph as pg
import xlsxwriter
from pyqtgraph.exporters import ImageExporter

from .methods.analysis import apply_SSA, get_density
from .methods.image_loading import load_hdf5_latest as load_hdf5
from .methods.reporting import create_profile_chart

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)


def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode="same")
    return y_smooth


def axes_pos_rel(ax, view):
    """
    Calculate the relative position and size of an axis within a view.
    Parameters:
    ax (object): The axis object for which the position and size are calculated.
    view (object): The view object that contains the axis.
    Returns:
    tuple: A tuple containing the relative x position, y position, width, and height of the axis within the view.
    """

    x0, y0, w, h = ax.geometry().getCoords()
    print("x0, y0, w, h", x0, y0, w, h)
    X0, Y0, W, H = view.geometry().getCoords()
    print("X0, Y0, W, H", X0, Y0, W, H)
    return x0 / W, y0 / H, w / W, h / H


class ImageForAnalysis:
    progress = 0

    def progress_update(self, name, dn):
        if hasattr(self, "_progress"):
            self._progress += dn
        else:
            self._progress = 1

    def __init__(self):
        self.total_refl_img: np.ndarray
        self.redcd_refl_img: np.ndarray
        self.px2mm: float
        self.offset_h: float
        self.aux_data: dict

    def load_from(self, path: Union[str, Path]):
        if isinstance(path, str):
            _tmp = load_hdf5(path)
        else:
            path = str(path)
            _tmp = load_hdf5(path)

        self.fp = path

        images: List
        px2mm: List[float]
        offset_h: List[float]

        images, px2mm, offset_h, aux_data = _tmp

        self.aux_data = aux_data
        print("aux data ", aux_data)

        self.total_refl_img = images[0][0] / 1024
        if images[1][0] is not None:
            self.redcd_refl_img = images[1][0] / 1024

        self.px2mm = px2mm
        self.offset_h = offset_h

        self._data = {}
        self._data["image_ngr"] = self.total_refl_img
        if images[1][0] is not None:
            self._data["image_gri"] = self.redcd_refl_img
        self._data["px2mm"] = self.px2mm

        try:
            self._data["wavelength"] = float(aux_data["wavelength"][:3])
        except Exception:
            self._data["wavelength"] = 940.0

    def calculate_SSA(self):
        self.SSA_image, self.R_framed, self.SSA_profile, self._Cal = apply_SSA(
            self._data["image_ngr"], self._data["wavelength"], self._data["px2mm"]
        )

    def calculate_rho(self):
        self.progress_update("Calculating density", 1)
        _out = get_density(
            self._data["image_ngr"],
            self._data["image_gri"],
            self.SSA_image,
            self._data["px2mm"],
        )
        self.progress_update("Loading images ... Done!", 100)

        (
            self.density_profiles,
            self.SSA_framed,
            self.R_masked,
            self.for_rho_masked,
            self.rho_cal,
        ) = _out

        self.density_profile = self.density_profiles[0]

    def pg_to_bytes(self, win, dim=(1600, 400)):
        # exporter.parameters()["width"] = dim[0]
        # exporter.parameters()["height"] = dim[1]

        # win.resize(dim[0], dim[1])
        # win.setFixedSize(dim[0], dim[1])

        # win.setGeometry(0, 0, dim[0]*2, dim[1])

        pg.mkQApp().processEvents()

        exporter = ImageExporter(win.scene())
        export_bo = exporter.export(toBytes=True)
        # out.scaledToHeight(dim[1])

        ba = pg.QtCore.QByteArray()
        bu = pg.QtCore.QBuffer(ba)

        export_bo.save(bu, "png")

        imgIO = BytesIO()
        imgIO.write(bu.data())
        imgIO.seek(0)

        return imgIO

    def generate_report(self, fp=None):
        axes = []

        grid_included = "image_gri" in self._data.keys()
        density_calculated = hasattr(self, "density_profiles")

        _R_min = 0.15
        _R_max = 0.95

        _R_framed = np.nanmean(self.R_framed, axis=1)
        _SSA_framed = self.SSA_profile

        _R_cal = self._Cal[0]
        _SSA_cal = self._Cal[1]

        print("Generating report ...")

        backend = "xlsx"

        _vmax = np.nanmax(self.SSA_profile) * 1.5

        height = self.px2mm * np.arange(int(self._data["image_ngr"].shape[0]))

        img = self._data["image_ngr"]

        extent = (0, img.shape[1] * self.px2mm, 0, img.shape[0] * self.px2mm)

        headers = ["index", "Height", "SSA"]
        df = [
            np.arange(0, len(height)),
            height,
            self.SSA_profile[::-1],
        ]

        if grid_included:  # "image_gri" in self._data.keys():
            # df.append(smooth(self.density_profile[::-1], 15))
            if density_calculated:
                for density_profile in self.density_profiles:
                    headers.append("Ice-volume fraction")
                    df.append(density_profile[::-1])

        _major_dim = 3 * 1.25
        _minor_dim = 2 * 1.25
        dpi = 96 * 2

        excel_file = fp
        data_sheet = "data"
        aux_data_sheet = "aux_data"
        meta_data_sheet = "meta_data"
        report_sheet = "report"

        workbook = xlsxwriter.Workbook(excel_file, {"nan_inf_to_errors": True})

        report_doc = workbook.add_worksheet(report_sheet)
        report_doc.hide_gridlines(2)
        report_doc.set_page_view(2)

        data = workbook.add_worksheet(data_sheet)

        for i in range(len(df)):
            data.write(0, i, headers[i])
            data.write_column(1, i, df[i])

        aux_data = workbook.add_worksheet(aux_data_sheet)
        meta_data = workbook.add_worksheet(meta_data_sheet)

        report_doc.write("A31", "Notes", workbook.add_format({"bold": True}))

        format = workbook.add_format()
        format.set_bottom(1)
        report_doc.merge_range(32, 0, 32, 8, "", format)

        report_doc.merge_range(34, 0, 34, 8, "", format)

        report_doc.merge_range(36, 0, 36, 8, "", format)

        report_doc.merge_range(38, 0, 38, 8, "", format)

        format = workbook.add_format(
            {
                "bold": True,
                # "size": 16,
                "color": "#ffffff",
                "bg_color": "#0099CC",
                "align": "center",
                "valign": "vcenter",
            }
        )

        report_doc.merge_range(
            0,
            0,
            1,
            8,
            "SnowImager report",
            format,
        )

        _format = workbook.add_format({"bg_color": "#eeeeee", "align": "right"})

        report_doc.merge_range(3, 0, 3, 1, "Observer: ", _format)
        report_doc.merge_range(
            4,
            0,
            4,
            1,
            "Date: ",
            workbook.add_format({"bg_color": "#eeeeee", "align": "right"}),
        )
        report_doc.merge_range(
            5,
            0,
            5,
            1,
            "Location: ",
            workbook.add_format({"bg_color": "#eeeeee", "align": "right"}),
        )
        report_doc.merge_range(
            6,
            0,
            6,
            1,
            "Weather: ",
            workbook.add_format({"bg_color": "#eeeeee", "align": "right"}),
        )
        report_doc.merge_range(
            7,
            0,
            7,
            1,
            "Temperature: ",
            workbook.add_format({"bg_color": "#eeeeee", "align": "right"}),
        )
        report_doc.merge_range(
            8,
            0,
            8,
            1,
            "Wind: ",
            workbook.add_format({"bg_color": "#eeeeee", "align": "right"}),
        )

        _format = workbook.add_format({})
        _format.set_bottom(1)

        report_doc.merge_range(3, 2, 3, 8, "", _format)

        if len(self.aux_data) > 0:
            report_doc.merge_range(4, 2, 4, 8, self.aux_data["timestamp"], _format)
        else:
            report_doc.merge_range(4, 2, 4, 8, "", _format)

        if len(self.aux_data) > 0:
            report_doc.merge_range(
                5,
                2,
                5,
                8,
                f"lon.: {self.aux_data['longitude']} lat.: {self.aux_data['latitude']}",
                _format,
            )
        else:
            report_doc.merge_range(5, 2, 5, 8, "", _format)

        report_doc.merge_range(6, 2, 6, 8, "", _format)

        if len(self.aux_data) > 0:
            report_doc.merge_range(
                7,
                2,
                7,
                8,
                f"{self.aux_data['board_temperature_led_side']} (from LED side electronics)",
                _format,
            )
        else:
            report_doc.merge_range(7, 2, 7, 8, "", _format)

        report_doc.merge_range(8, 2, 8, 8, "", _format)

        report_doc.merge_range(
            10,
            0,
            10,
            2,
            "SSA measurement",
            workbook.add_format({"color": "#0099CC", "bold": True}),
        )

        aux_data.merge_range(
            0,
            0,
            0,
            8,
            "Use this worksheet to store auxiliary data from, e.g., density cutter, "
            + "InfraSnow, SLF-Sensor, IceCube, micro-CT, etc. and plot it in the report.",
            workbook.add_format(
                {"bold": True, "text_wrap": True, "bg_color": "#ffe38e"}
            ),
        )

        aux_data.merge_range(
            1, 0, 1, 1, "Instrument A", workbook.add_format({"bold": True})
        )
        aux_data.write("A3", "Height / mm")
        aux_data.write("B3", "Data A")

        aux_data.merge_range(
            1, 2, 1, 3, "Instrument B", workbook.add_format({"bold": True})
        )
        aux_data.write("C3", "Height / mm")
        aux_data.write("D3", "Data B")

        aux_data.merge_range(1, 4, 1, 5, "...", workbook.add_format({"bold": True}))

        if len(self.aux_data) > 0:
            meta_data.write("A1", "no grid")
            i_aux = 2
            for key, val in self.aux_data.items():
                meta_data.write(f"A{i}", key)
                meta_data.write(f"B{i}", val)
                i_aux += 1

        report_doc.merge_range(
            44,
            0,
            44,
            8,
            "This is an auto-generated report from SnowImagerPro (Davos Instruments//SLF)",
            workbook.add_format({"italic": True}),
        )

        # SSA image
        data = self._data["image_ngr"].T
        w, h = data.shape
        ratio = h / w

        # define image size
        H = int(500)
        W = int(H / ratio)
        png_geometry = (0, 0, W, H)

        # define plot size
        pw = png_geometry[2] - 50
        ph = png_geometry[3] - 50

        # relative position of the plot within the image
        plt_pos = (0, 0, pw / W, ph / H)
        print("plt_pos", plt_pos)

        plt1 = pg.GraphicsLayoutWidget()  # show=False, size=(600, 400))
        plt1.setBackground("w")
        print("WIndow geometry", png_geometry)
        plt1.setGeometry(*png_geometry)

        qlayout = plt1.ci.layout
        qlayout.setColumnFixedWidth(0, pw)
        qlayout.setRowFixedHeight(0, ph)

        p1 = plt1.addPlot(0, 0)
        axes.extend([p1])

        p1.getViewBox().setDefaultPadding(0)
        print(p1.getViewBox().viewRect())
        p1.setAspectLocked(True)

        img = pg.ImageItem(
            data,
            levels=(_R_min, _R_max),
            pen=pg.mkPen(color="b", width=2),
            symbol="o",
            symbolSize=5,
            symbolBrush=("r"),
        )

        tr = pg.QtGui.QTransform()
        px2mm = self.px2mm
        tr.scale(px2mm, px2mm)

        img.setTransform(tr)

        img_SSA = pg.ImageItem(
            self.SSA_image.T,
            levels=(0, _vmax),
            colorMap=pg.colormap.get("CET-L8"),  # CET-L8, CET-R1
        )

        img_SSA.setTransform(tr)

        # p1.setYRange(0, h * px2mm)
        # p1.setXRange(0, w * px2mm)

        p1.addItem(img)
        p1.addItem(img_SSA)

        p1.setLabel("bottom", "Width / mm")
        p1.setLabel("left", "Height in snowpit / mm")

        plt2 = pg.GraphicsLayoutWidget()
        plt2.setBackground("w")
        plt2.setGeometry(*png_geometry)

        qlayout2 = plt2.ci.layout
        qlayout2.setColumnFixedWidth(0, pw)
        qlayout2.setRowFixedHeight(0, ph)

        p2 = plt2.addPlot(0, 0)
        axes.extend([p2])

        p2.plot(_R_cal, _SSA_cal, pen=pg.mkPen(color="b", width=2))

        p2.setLabel("bottom", "Reflectance")
        p2.setLabel("left", "SSA / (m² kg⁻¹)")

        p2.setXRange(_R_min, _R_max)
        p2.setYRange(0, _vmax)

        axis_font = pg.QtGui.QFont("Arial", 14)
        label_font = pg.QtGui.QFont("Arial", 14)

        if grid_included and density_calculated:
            plt3 = pg.GraphicsLayoutWidget()
            plt3.setBackground("w")

            wide_geometry = (0, 0, W * 3, H)
            plt3.setGeometry(*wide_geometry)

            p3_1 = plt3.addPlot(0, 0)
            p3_2 = plt3.addPlot(0, 1)

            _tmp = np.nansum(self.R_masked, axis=0)
            _tmp[_tmp == 0] = np.nan

            p3_refl = pg.ImageItem(
                self._data["image_ngr"].T,
                levels=(_R_min, _R_max),
            )
            p3_refl.setTransform(tr)

            p3_1.addItem(p3_refl)

            p3_grid_refl = pg.ImageItem(
                _tmp.T,
                levels=(_R_min, _R_max),
                colorMap=pg.colormap.get("CET-L8"),
            )

            p3_grid_refl.setTransform(tr)

            p3_1.addItem(p3_grid_refl)

            p3_1.setXRange(0, w * px2mm)
            p3_1.setYRange(0, h * px2mm)

            axes.extend([p3_1])

            p3_grid = pg.ImageItem(
                self._data["image_gri"].T,
                levels=(_R_min, _R_max),
            )

            p3_grid.setTransform(tr)

            p3_2.addItem(p3_grid)

            p3_2.setXRange(0, w * px2mm)
            p3_2.setYRange(0, h * px2mm)

            axes.extend([p3_2])

            _d_opt = np.geomspace(0.01, 60, 100)
            R = np.linspace(0, 1, 100)
            xx, yy = np.meshgrid(R, _d_opt / 1000)

            r = 12.5

            _tmp = self.rho_cal(xx, yy, r) - 0.35

            # p3_3 = plt3.addPlot(0,2)
        #
        # p3_cal = pg.ImageItem(
        #    _tmp,
        #    ColorMap = pg.colormap.get("CET-L8"),
        #    levels=(0, _vmax),
        # )
        #
        # p3_3.addItem(p3_cal)
        #
        # axes.extend([p3_3])

        for p in axes:
            p.getAxis("left").setPen(pg.mkPen(color="k"))
            p.getAxis("bottom").setPen(pg.mkPen(color="k"))
            # Set axis numbers to black
            p.getAxis("left").setTextPen(pg.mkPen(color="k"))
            p.getAxis("bottom").setTextPen(pg.mkPen(color="k"))
            # Add a box around the plot
            p.getViewBox().setBorder(color="k", width=2)
            # Increase tick width
            p.getAxis("left").setTickPen(pg.mkPen(width=2, color="k"), length=10)
            p.getAxis("bottom").setTickPen(pg.mkPen(width=2, color="k"), length=10)
            # Set minor ticks color to black
            p.getAxis("left").setTickPen(pg.mkPen(width=2, color="k"), minor=True)
            p.getAxis("bottom").setTickPen(pg.mkPen(width=2, color="k"), minor=True)
            # Set axis font
            p.getAxis("left").setStyle(tickFont=axis_font, tickTextOffset=5)
            p.getAxis("bottom").setStyle(tickFont=axis_font, tickTextOffset=5)
            # Set label font
            p.getAxis("bottom").label.setFont(label_font)
            p.getAxis("left").label.setFont(label_font)
            # Set plot line width
            colors = ["b", "r", "g", "c", "m", "y", "k", "w"]
            for color, item in zip(colors, p.items):
                if isinstance(item, pg.PlotDataItem):
                    item.setPen(pg.mkPen(width=2, color=color))

        # p1.setYRange(0, h)

        imgIO = self.pg_to_bytes(plt1, dim=(400, 600))

        scale = 0.5
        report_doc.insert_image(
            12,
            0,
            "",
            {
                "image_data": imgIO,
                "x_scale": scale,
                "y_scale": scale,
                "object_position": 2,
            },
        )

        # p1.getViewBox().autoRange()

        plt_pos = axes_pos_rel(p1, plt1)
        print("mpl style pos", plt_pos)

        SSA_chart = create_profile_chart(
            workbook,
            data_sheet,
            2,
            1,
            len(df[0]),
            "SSA / (mm² kg\u207b¹)",
            "Height / mm",
            W=int(_minor_dim * scale * dpi),
            H=int(_major_dim * scale * dpi),
            x_axis={"min": 0, "max": _vmax},
            plt_pos=plt_pos,
        )

        SSA_chart.add_series(
            {
                "name": [aux_data_sheet, 1, 0],
                "values": [aux_data_sheet, 3, 0, 10000, 0],
                "categories": [aux_data_sheet, 3, 1, 10000, 1],
                "line": {"width": 1.0},
            }
        )

        report_doc.insert_chart(12, 3, SSA_chart)

        imgIO2 = self.pg_to_bytes(plt2, dim=(400, 600))

        report_doc.insert_image(
            12,
            10,
            "",
            {
                "image_data": imgIO2,
                "x_scale": scale,
                "y_scale": scale,
                "object_position": 2,
            },
        )

        if grid_included and density_calculated:
            imgIO3 = self.pg_to_bytes(plt3, dim=(400, 600))

            report_doc.insert_image(
                47,
                0,
                "",
                {
                    "image_data": imgIO3,
                    "x_scale": scale,
                    "y_scale": scale,
                    "object_position": 2,
                },
            )

            density_chart = create_profile_chart(
                workbook,
                data_sheet,
                [3, 4, 5, 6],
                [1] * 4,
                len(df[0]),
                "Ice-volume fraction",
                "Height / mm",
                W=int(_minor_dim * scale * dpi / 2),
                H=int(_major_dim * scale * dpi / 2),
                x_axis={"min": 0, "max": 0.55},
                plt_pos=plt_pos,
            )

            report_doc.insert_chart(47, 6, density_chart)

            report_doc.merge_range(
                45,
                0,
                45,
                2,
                "Density measurement",
                workbook.add_format({"color": "#0099CC", "bold": True}),
            )

            report_doc.write("A76", "Notes", workbook.add_format({"bold": True}))

            format = workbook.add_format()
            format.set_bottom(1)
            report_doc.merge_range(77, 0, 77, 8, "", format)

            report_doc.merge_range(79, 0, 79, 8, "", format)

            report_doc.merge_range(81, 0, 81, 8, "", format)

            report_doc.merge_range(83, 0, 83, 8, "", format)

            report_doc.merge_range(
                89,
                0,
                89,
                8,
                "This is an auto-generated report from SnowImagerPro (Davos Instruments//SLF)",
                workbook.add_format({"italic": True}),
            )

            if len(self.aux_data) > 0:
                meta_data.write(f"A{i_aux}", "grid")
                i_aux += 1
                for key, val in self.aux_data.items():
                    meta_data.write(f"A{i}", key)
                    meta_data.write(f"B{i}", val)
                    i_aux += 1

        workbook.close()

        print(f"Report saved to {fp}")

    def _generate_report(self, fp=None):
        plt.rcParams["text.usetex"] = False
        plt.rcParams["font.family"] = "serif"
        plt.rcParams["font.serif"] = [
            "NotoSerif NF",
            "CMU Serif",
            "DejaVu Serif",
            "Times New Roman",
        ]
        plt.rcParams["axes.linewidth"] = 1.5
        plt.rcParams["font.size"] = 8
        plt.rc("legend", fontsize=7)
        plt.rcParams["axes.labelsize"] = 10
        plt.rcParams["xtick.labelsize"] = 10
        plt.rcParams["ytick.labelsize"] = 10
        plt.rcParams["axes.edgecolor"] = "#2a2a2a"
        plt.rcParams["xtick.major.width"] = 1.5
        plt.rcParams["xtick.minor.width"] = 1.5
        plt.rcParams["ytick.major.width"] = 1.5
        plt.rcParams["ytick.minor.width"] = 1.5

        author = {"Creator": "SnowImagerPro"}

        _R_min = 0.15
        _R_max = 0.95

        _R_framed = np.nanmean(self.R_framed, axis=1)
        _SSA_framed = self.SSA_profile

        _R_cal = self._Cal[0]
        _SSA_cal = self._Cal[1]

        print("Generating report ...")

        backend = "xlsx"

        if backend == "xlsx":
            if fp is None:
                fp = "tests/report.xlsx"

            _vmax = np.nanmax(self.SSA_profile) * 1.5

            height = self.px2mm * np.arange(int(self._data["image_ngr"].shape[0]))

            img = self._data["image_ngr"]
            extent = (0, img.shape[1] * self.px2mm, 0, img.shape[0] * self.px2mm)

            headers = ["index", "Height", "SSA"]
            df = [
                np.arange(0, len(height)),
                height,
                self.SSA_profile[::-1],
            ]

            if "image_gri" in self._data.keys():
                # df.append(smooth(self.density_profile[::-1], 15))
                for density_profile in self.density_profiles:
                    headers.append("Ice-volume fraction")
                    df.append(density_profile[::-1])

            _major_dim = 3 * 1.25
            _minor_dim = 2 * 1.25
            dpi = 96 * 2

            excel_file = fp
            data_sheet = "data"
            aux_data_sheet = "aux_data"
            meta_data_sheet = "meta_data"
            report_sheet = "report"

            workbook = xlsxwriter.Workbook(excel_file, {"nan_inf_to_errors": True})

            report_doc = workbook.add_worksheet(report_sheet)
            report_doc.hide_gridlines(2)
            report_doc.set_page_view(2)

            data = workbook.add_worksheet(data_sheet)

            for i in range(len(df)):
                data.write(0, i, headers[i])
                data.write_column(1, i, df[i])

            aux_data = workbook.add_worksheet(aux_data_sheet)
            meta_data = workbook.add_worksheet(meta_data_sheet)

            report_doc.write("A31", "Notes", workbook.add_format({"bold": True}))

            format = workbook.add_format()
            format.set_bottom(1)
            report_doc.merge_range(32, 0, 32, 8, "", format)

            report_doc.merge_range(34, 0, 34, 8, "", format)

            report_doc.merge_range(36, 0, 36, 8, "", format)

            report_doc.merge_range(38, 0, 38, 8, "", format)

            # SSA image
            imgdata = BytesIO()
            fig, ax = plt.subplots(
                figsize=(_minor_dim, _major_dim),
            )
            ax.imshow(self._data["image_ngr"], cmap="gray", extent=extent)
            im = ax.imshow(
                self.SSA_image,
                cmap="rainbow",
                vmin=0,
                vmax=_vmax,
                alpha=0.75,
                extent=extent,
            )
            ax.set_xlabel("x / mm")
            ax.set_ylabel("y / mm")

            ax.tick_params("both", length=6, width=1.5, which="major")
            ax.tick_params(axis="x", pad=8)  #
            # ax.xaxis.labelpad = 8

            plt.colorbar(
                im,
                ax=ax,
                orientation="horizontal",
                location="top",
                label="SSA / (m² kg⁻¹)",
            )
            plt.tight_layout()

            # TODO: trying to offset plot to avoid ods chart to change size. doesnt work yet >> Use ODSCHARTS
            _pos = ax.get_position()
            ax.set_position([_pos.x0, _pos.y0 + 0.05, _pos.width, _pos.height - 0.05])

            fig.savefig(
                imgdata,
                format="png",
                dpi=dpi,
            )  # facecolor="black")
            imgdata.seek(0)

            ax_pos = ax.get_position()

            plt_pos = (ax_pos.x0, ax_pos.y0, ax_pos.width, ax_pos.height)

            scale = 0.75
            report_doc.insert_image(
                12,
                0,
                "",
                {
                    "image_data": imgdata,
                    "x_scale": scale,
                    "y_scale": scale,
                    "object_position": 2,
                },
            )

            SSA_chart = create_profile_chart(
                workbook,
                data_sheet,
                2,
                1,
                len(df[0]),
                "SSA / (mm² kg\u207b¹)",
                "Height / mm",
                W=int(_minor_dim * scale * dpi / 2),
                H=int(_major_dim * scale * dpi / 2),
                x_axis={"min": 0, "max": _vmax},
                plt_pos=plt_pos,
            )

            SSA_chart.add_series(
                {
                    "name": [aux_data_sheet, 1, 0],
                    "values": [aux_data_sheet, 3, 0, 10000, 0],
                    "categories": [aux_data_sheet, 3, 1, 10000, 1],
                    "line": {"width": 1.0},
                }
            )

            report_doc.insert_chart(12, 3, SSA_chart)

            imgdata = BytesIO()
            fig, ax = plt.subplots(1, 1, figsize=(_minor_dim, _major_dim))
            ax.plot(_R_cal, _SSA_cal, label="Calibration")
            ax.scatter(
                _R_framed[::20],
                _SSA_framed[::20],
                marker="x",
                color="red",
                label="Data",
                alpha=0.25,
            )
            ax.set_xlabel("Reflectance")
            ax.set_ylabel("SSA / (m² kg⁻¹)")
            ax.set_xlim(0, 1)
            ax.set_ylim(0, _vmax)
            ax.legend()
            plt.tight_layout()

            ax.set_position(ax_pos)

            fig.savefig(imgdata, format="png", dpi=dpi)
            imgdata.seek(0)

            report_doc.insert_image(
                12,
                6,
                "",
                {
                    "image_data": imgdata,
                    "x_scale": 0.75,
                    "y_scale": 0.75,
                    "object_position": 2,
                },
            )

            format = workbook.add_format(
                {
                    "bold": True,
                    "size": 16,
                    "color": "#ffffff",
                    "bg_color": "#0099CC",
                    "align": "center",
                    "valign": "vcenter",
                }
            )

            report_doc.merge_range(
                0,
                0,
                1,
                8,
                "SnowImager report",
                format,
            )

            _format = workbook.add_format({"bg_color": "#eeeeee", "align": "right"})

            report_doc.merge_range(3, 0, 3, 1, "Observer: ", _format)
            report_doc.merge_range(
                4,
                0,
                4,
                1,
                "Date: ",
                workbook.add_format({"bg_color": "#eeeeee", "align": "right"}),
            )
            report_doc.merge_range(
                5,
                0,
                5,
                1,
                "Location: ",
                workbook.add_format({"bg_color": "#eeeeee", "align": "right"}),
            )
            report_doc.merge_range(
                6,
                0,
                6,
                1,
                "Weather: ",
                workbook.add_format({"bg_color": "#eeeeee", "align": "right"}),
            )
            report_doc.merge_range(
                7,
                0,
                7,
                1,
                "Temperature: ",
                workbook.add_format({"bg_color": "#eeeeee", "align": "right"}),
            )
            report_doc.merge_range(
                8,
                0,
                8,
                1,
                "Wind: ",
                workbook.add_format({"bg_color": "#eeeeee", "align": "right"}),
            )

            _format = workbook.add_format({})
            _format.set_bottom(1)

            report_doc.merge_range(3, 2, 3, 8, "", _format)

            if len(self.aux_data) > 0:
                report_doc.merge_range(4, 2, 4, 8, self.aux_data["timestamp"], _format)
            else:
                report_doc.merge_range(4, 2, 4, 8, "", _format)

            if len(self.aux_data) > 0:
                report_doc.merge_range(
                    5,
                    2,
                    5,
                    8,
                    f"lon.: {self.aux_data['longitude']} lat.: {self.aux_data['latitude']}",
                    _format,
                )
            else:
                report_doc.merge_range(5, 2, 5, 8, "", _format)

            report_doc.merge_range(6, 2, 6, 8, "", _format)

            if len(self.aux_data) > 0:
                report_doc.merge_range(
                    7,
                    2,
                    7,
                    8,
                    f"{self.aux_data['board_temperature_led_side']} (from LED side electronics)",
                    _format,
                )
            else:
                report_doc.merge_range(7, 2, 7, 8, "", _format)

            report_doc.merge_range(8, 2, 8, 8, "", _format)

            report_doc.merge_range(
                10,
                0,
                10,
                2,
                "SSA measurement",
                workbook.add_format({"color": "#0099CC", "bold": True}),
            )

            aux_data.merge_range(
                0,
                0,
                0,
                8,
                "Use this worksheet to store auxiliary data from, e.g., density cutter, "
                + "InfraSnow, SLF-Sensor, IceCube, micro-CT, etc. and plot it in the report.",
                workbook.add_format(
                    {"bold": True, "text_wrap": True, "bg_color": "#ffe38e"}
                ),
            )

            aux_data.merge_range(
                1, 0, 1, 1, "Instrument A", workbook.add_format({"bold": True})
            )
            aux_data.write("A3", "Height / mm")
            aux_data.write("B3", "Data A")

            aux_data.merge_range(
                1, 2, 1, 3, "Instrument B", workbook.add_format({"bold": True})
            )
            aux_data.write("C3", "Height / mm")
            aux_data.write("D3", "Data B")

            aux_data.merge_range(1, 4, 1, 5, "...", workbook.add_format({"bold": True}))

            if len(self.aux_data) > 0:
                meta_data.write("A1", "no grid")
                i_aux = 2
                for key, val in self.aux_data.items():
                    meta_data.write(f"A{i}", key)
                    meta_data.write(f"B{i}", val)
                    i_aux += 1

            report_doc.merge_range(
                44,
                0,
                44,
                8,
                "This is an auto-generated report from SnowImagerPro (Davos Instruments//SLF)",
                workbook.add_format({"italic": True}),
            )

            ############################################################
            #########################  DENSTIY #########################
            ############################################################

            if "image_gri" in self._data.keys():
                _tmp = np.nansum(self.R_masked, axis=0)
                _tmp[_tmp == 0] = np.nan

                imgdata = BytesIO()
                fig, ax = plt.subplots(1, 2, figsize=(_minor_dim * 2, _major_dim))
                ax[0].imshow(self._data["image_ngr"], cmap="gray", extent=extent)
                im = ax[0].imshow(
                    _tmp,
                    cmap="rainbow",
                    vmin=_R_min,
                    vmax=_R_max,
                    alpha=0.75,
                    extent=extent,
                )
                ax[1].imshow(self._data["image_gri"], cmap="gray", extent=extent)
                for _img in self.for_rho_masked:
                    ax[1].imshow(
                        _img,
                        cmap="rainbow",
                        vmin=_R_min,
                        vmax=_R_max,
                        alpha=0.75,
                        extent=extent,
                    )

                ax[0].set_xlabel("x / mm")
                ax[0].set_ylabel("y / mm")
                ax[0].tick_params("both", length=6, width=1.5, which="major")
                ax[1].set_xlabel("x / mm")
                ax[1].set_yticks([])
                ax[1].tick_params("both", length=6, width=1.5, which="major")

                for _ax in ax:
                    _ax.tick_params(axis="x", pad=8)

                plt.tight_layout()

                ax0_pos = ax[0].get_position()
                ax[0].set_position(
                    [ax0_pos.x0, ax0_pos.y0, ax0_pos.width, ax0_pos.height - 0.1]
                )
                ax1_pos = ax[1].get_position()
                ax[1].set_position(
                    [ax1_pos.x0, ax1_pos.y0, ax1_pos.width, ax1_pos.height - 0.1]
                )

                cbar_ax = fig.add_axes(
                    [ax0_pos.x0, 0.85, ax0_pos.width + ax1_pos.width, 0.03]
                )
                fig.colorbar(
                    im,
                    cax=cbar_ax,
                    label="Reflectance",
                    orientation="horizontal",
                    location="top",
                )

                fig.savefig(imgdata, format="png", dpi=dpi)
                imgdata.seek(0)

                ax_pos = ax[0].get_position()
                plt_pos = (ax_pos.x0 * 2, ax_pos.y0, ax_pos.width * 2, ax_pos.height)

                report_doc.insert_image(
                    47,
                    0,
                    "",
                    {
                        "image_data": imgdata,
                        "x_scale": 0.75,
                        "y_scale": 0.75,
                        "object_position": 2,
                    },
                )

                density_chart = create_profile_chart(
                    workbook,
                    data_sheet,
                    [3, 4, 5, 6],
                    [1] * 4,
                    len(df[0]),
                    "Ice-volume fraction",
                    "Height / mm",
                    W=int(_minor_dim * scale * dpi / 2),
                    H=int(_major_dim * scale * dpi / 2),
                    x_axis={"min": 0, "max": 0.55},
                    plt_pos=plt_pos,
                )

                report_doc.insert_chart(47, 6, density_chart)

                report_doc.merge_range(
                    45,
                    0,
                    45,
                    2,
                    "Density measurement",
                    workbook.add_format({"color": "#0099CC", "bold": True}),
                )

                report_doc.write("A76", "Notes", workbook.add_format({"bold": True}))

                format = workbook.add_format()
                format.set_bottom(1)
                report_doc.merge_range(77, 0, 77, 8, "", format)

                report_doc.merge_range(79, 0, 79, 8, "", format)

                report_doc.merge_range(81, 0, 81, 8, "", format)

                report_doc.merge_range(83, 0, 83, 8, "", format)

                report_doc.merge_range(
                    89,
                    0,
                    89,
                    8,
                    "This is an auto-generated report from SnowImagerPro (Davos Instruments//SLF)",
                    workbook.add_format({"italic": True}),
                )

                if len(self.aux_data) > 0:
                    meta_data.write(f"A{i_aux}", "grid")
                    i_aux += 1
                    for key, val in self.aux_data.items():
                        meta_data.write(f"A{i}", key)
                        meta_data.write(f"B{i}", val)
                        i_aux += 1

                _d_opt = np.geomspace(0.01, 60, 100)
                R = np.linspace(0, 1, 100)
                xx, yy = np.meshgrid(R, _d_opt / 1000)

                r = 12.5

                _tmp = self.rho_cal(xx, yy, r) - 0.35

                cmp = colormaps["rainbow"]
                cmp.set_over(color="w")
                cmp.set_under(color="w")

                imgdata = BytesIO()
                fig, ax = plt.subplots(1, 1, figsize=(_major_dim, _major_dim))
                im = ax.pcolormesh(R, _d_opt, _tmp, cmap=cmp, vmin=0, vmax=1)
                ax.contour(
                    R,
                    _d_opt,
                    _tmp,
                    levels=np.arange(0, 1, 0.1),
                    colors="black",
                    alpha=0.5,
                )

                _tmp = np.nanmean(self.for_rho_masked[0], axis=1)

                H = ax.scatter(
                    _tmp[::15],
                    6 / self.SSA_profile[::-15],
                    c=height[::15],
                    s=5,
                    cmap="Greys",
                    zorder=10,
                )

                fig.colorbar(im, location="top", label="Ice-volume fraction")
                fig.colorbar(H, ax=ax, label="height / mm")

                ax.set_yscale("log")

                ax.set_xlabel("Reduced reflectance")
                ax.set_ylabel("Optical diameter / mm")

                # ax.set_position((plt_pos[0], plt_pos[1], plt_pos[3], plt_pos[3]))
                plt.tight_layout()
                fig.savefig(imgdata, format="png", dpi=dpi)
                imgdata.seek(0)
                report_doc.insert_image(
                    61,
                    1,
                    "",
                    {
                        "image_data": imgdata,
                        "x_scale": 0.75,
                        "y_scale": 0.75,
                        "object_position": 2,
                    },
                )

            workbook.close()

            print(f"Report saved to {fp}")

        elif backend == "ods":
            report_doc = SpreadSheet()

            list_of_rows = [
                ["Altitude", "Pressure"],
                ["feet", "psia"],
                [0, 14.7],
                [5000, 12.23],
                [10000, 10.11],
                [30000, 4.36],
                [60000, 1.04],
            ]

            report_doc.add_sheet("Alt_Data", list_of_rows)

            report_doc.add_scatter(
                "Alt_P_Plot",
                "Alt_Data",
                title="Pressure vs Altitude",
                xlabel="Altitude",
                ylabel="Pressure",
                xcol=1,
                ycolL=[2],
            )
            report_doc.save(filename=fp)
