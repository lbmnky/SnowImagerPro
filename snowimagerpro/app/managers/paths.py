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

import os

from platformdirs import user_config_dir, user_data_dir

from snowimagerpro import __APPNAME__, __ORGNAME__

base = user_data_dir(appname=__APPNAME__)
data_dir = user_data_dir(appname=__APPNAME__)
conf_dir = user_config_dir(appname=__ORGNAME__)

# this is a fix to match QSettings path
# TODO: CHECK WIN/MAC


class Paths:
    basepath = "."
    resources = os.path.join(basepath, "resources")

    @classmethod
    def resource(cls, item):
        return os.path.join(cls.resources, item)

    @classmethod
    def set_basepath(cls, basepath):
        cls.basepath = basepath
        cls.resources = os.path.join(cls.basepath, "resources")


paths = Paths()
