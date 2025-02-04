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
from typing import Union

from pyqtconfig import ConfigManager, QSettingsManager

from snowimagerpro import __APPNAME__
from snowimagerpro.app.managers.paths import conf_dir


class Settings(QSettingsManager):
    def __init__(self):
        """Postpone till after QApplication is initialized"""
        pass

    def initialize(self):
        super(Settings, self).__init__()

        # Check if settings exist and if not, create them
        if not self.get("config_file"):
            self.set("config_file", os.path.join(conf_dir, f"{__APPNAME__}.json"))


class UserConfig(ConfigManager):
    _default: dict[str, Union[dict, int, str, list]] = {
        "raw_image_dbs": {},
        "raw_image_dbs_last": 0,
        "processed_image_dbs": {},
        "initial_tab": 1,
        "inspector.defaultDirs": [os.path.expanduser("~")],
        "explorer.db_path": os.path.expanduser("~"),
        "explorer.autosave": False,
        "processor.sortby": "date",
        "processor.overlap_x": 100,
        "processor.overlap_y": 100,
        "processor.h5_path": os.path.expanduser("~"),
        "analyzer.db_path": os.path.expanduser("~"),
        "analyzer.data_dir": os.path.expanduser("~"),
        "report.path": os.path.expanduser("~"),
    }

    def __init__(self):
        """Postpone till after QApplication is initialized"""

    def initialize(self):
        super(UserConfig, self).__init__(
            defaults=self._default, filename=settings.get("config_file")
        )

        # Adds new settings to the config file if they don't exist
        self.save()


settings = Settings()
user_config = UserConfig()
