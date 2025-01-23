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

from PySide6.QtCore import Slot

from workers.base import WorkerBase


class Worker(WorkerBase):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)
        # Store constructor arguments (re-used for processing)
        self.fn = fn

    @Slot()
    def do(self):
        return self.fn(*self.args, **self.kwargs)
