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

from PySide6.QtCore import QObject, Slot

from snowimagerpro.app.plugins import __plugins__

logger = "managers.plugins"


class Plugins:
    def __init__(self):
        pass

    def load(self):
        self.plugins = __plugins__

    def init(self):
        for name, model, view, logic in plugins.plugins:
            view.initialize()

            logic.update.connect(plugins.update)

    def post_init(self):
        for name, model, view, logic in plugins.plugins:
            ## TODO: move to view_base
            try:
                view.post_init()
            except AttributeError:
                logging.getLogger(logger).info(
                    f"post_init NOT implemented for plugin {name} (view)"
                )

            try:
                logic.post_init()
            except AttributeError:
                logging.getLogger(logger).info(
                    f"post_init NOT implemented for plugin {name} (logic)"
                )

    @Slot(QObject)
    def update(self, obj):
        print(f"emitted from {obj}")
        for plugin in self.plugins:
            plugin.model.do_update()

    def bla_update(self):
        print("Bla updoot")


plugins = Plugins()
