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
import os
import signal
import sys
from logging.handlers import RotatingFileHandler

from PySide6.QtWidgets import QApplication

from snowimagerpro import __APPNAME__, __DOMAIN__, __ORGNAME__, __VERSION__
from snowimagerpro.app.main_view import MainView
from snowimagerpro.app.managers import paths, plugins, settings, user_config
from snowimagerpro.app.plugins.base import public_data

signal.signal(signal.SIGINT, signal.SIG_DFL)  # Handle Ctrl+C

logging.basicConfig(
    handlers=[RotatingFileHandler("debug.log", maxBytes=100000, backupCount=1)],
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

logger = "__main__"


def main(BASE_PATH):
    logging.getLogger(logger).info(f"Starting {__APPNAME__} v{__VERSION__}")

    paths.set_basepath(BASE_PATH)

    app = QApplication()
    app.setApplicationName(__APPNAME__)
    app.setOrganizationName(__ORGNAME__)
    app.setOrganizationDomain(__DOMAIN__)

    settings.initialize()

    user_config.initialize()
    logging.getLogger(logger).info("User config initialized.")
    logging.getLogger(logger).info(f"Config file: {settings.get('config_file')}")

    public_data.initialize()
    logging.getLogger(logger).info("Shared data initialized.")

    plugins.load()
    logging.getLogger(logger).info("Plugins loaded.")

    plugins.init()
    logging.getLogger(logger).info("Plugins initialized.")

    win = MainView(
        title=f"{__APPNAME__} v{__VERSION__}",
        icon_path=paths.resource("icons/SnowImagerPro.ico"),
        theme_path=paths.resource("themes/dark.qss"),
    )

    plugins.post_init()
    logging.getLogger(logger).info("Plugins running post_init.")

    print("ALL SET UP!")
    logging.getLogger(logger).info("All set up.")

    public_data.change_selected_db(user_config.get("raw_image_dbs_last"))
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main(os.path.dirname(os.path.abspath(__file__)))
