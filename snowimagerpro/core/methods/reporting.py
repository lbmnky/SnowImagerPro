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


def create_profile_chart(
    workbook,
    sheet,
    col_x,
    col_y,
    max_row,
    xlabel,
    ylabel,
    W=200,
    H=300,
    x_axis={},
    y_axis={},
    plt_pos=(0.1, 0.1, 0.8, 0.8),
):
    x0, y0, w0, h0 = plt_pos

    chart = workbook.add_chart(
        {
            "type": "scatter",
            "subtype": "straight",
        }
    )

    if not isinstance(col_x, list):
        col_x = [col_x]
    if not isinstance(col_y, list):
        col_y = [col_y]

    for x, y in zip(col_x, col_y):
        chart.add_series(
            {
                "name": "SnowImager",
                "values": [sheet, 1, y, max_row, y],
                "categories": [sheet, 1, x, max_row, x],
                "line": {"width": 1.0},
            }
        )

    chart.set_title({"none": True})

    chart.set_x_axis(
        {
            **x_axis,
            **{
                "name": xlabel,
                "position_axis": "on_tick",
                "name_font": {
                    "name": "LM Roman 10",
                    "size": 8,
                    "color": "#111111",
                    "bold": True,
                },
                "num_font": {
                    "name": "LM Roman 10",
                    "size": 8,
                    "color": "#111111",
                    "bold": True,
                },
                "line": {"color": "#111111", "width": 1.0},
            },
        }
    )
    chart.set_y_axis(
        {
            **y_axis,
            **{
                "name": ylabel,
                "major_gridlines": {"visible": False},
                "name_font": {
                    "name": "LM Roman 10",
                    "size": 8,
                    "color": "#111111",
                    "bold": True,
                },
                "num_font": {
                    "name": "LM Roman 10",
                    "size": 8,
                    "color": "#111111",
                    "bold": True,
                },
                "line": {"color": "#111111", "width": 1.0},
            },
        }
    )

    chart.set_size({"width": W, "height": H})

    # Calculate axis size from MPL figure
    a = x0 * W
    b = (1 - h0 - y0) * H
    w = w0 * W
    h = h0 * H

    x = a / W
    y = b / H
    width = w / W
    height = h / H

    chart.set_plotarea(
        {
            "border": {"color": "black", "width": 1.0},
            "layout": {"x": x, "y": y, "width": width, "height": height},
        }
    )
    chart.set_chartarea(
        {
            "border": {"none": True},
        }
    )  # "fill": {"color": "gray"}})

    chart.set_legend(
        {
            "position": "overlay_right",
            "layout": {
                "x": 0.40,
                "y": 0.1,
                "width": 0.52,
                "height": 0.08,
            },
            "font": {
                "name": "LM Roman 10",
                "size": 6,
                "color": "#111111",
            },
            "fill": {"color": "#eeeeee", "transparency": 50},
        }
    )

    return chart
