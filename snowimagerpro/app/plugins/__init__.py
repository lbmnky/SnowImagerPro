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


from collections import namedtuple

from . import about, db_explorer, image_analyzer, image_inspector, image_processor

__all__ = [
    "image_inspector",
    "db_explorer",
    "image_processor",
    "image_analyzer",
    "about",
]

Plugin = namedtuple("Plugin", ["name", "model", "view", "logic"])

__plugins__ = [
    Plugin(*image_inspector.plugin),
    Plugin(*db_explorer.plugin),
    Plugin(*image_processor.plugin),
    Plugin(*image_analyzer.plugin),
    Plugin(*about.plugin),
]
