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

from . import methods
from .analysis import ImageForAnalysis
from .metadata import ImageMetadata
from .processing import Image, ImageSet
from ._GLOBALS import DEBUG


def toggle_debug(*args):
    global DEBUG
    print(DEBUG)
    if args:
        DEBUG = args[0]
    elif len(args) > 1:
        logging.warning("toggle_debug takes only one argument")
    else:
        DEBUG = not DEBUG
    print(DEBUG)


__all__ = [
    "Image",
    "ImageSet",
    "ImageForAnalysis",
    "ImageMetadata",
    "toggle_debug",
    "DEBUG",
    "methods",
]
