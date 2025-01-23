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
import traceback

from PySide6.QtCore import QObject, QRunnable, Signal, Slot


class WorkerSignals(QObject):
    started = Signal()
    complete = Signal()  # Success.
    finished = Signal()
    progress = Signal(int)
    error = Signal(Exception)
    result = Signal(
        object
    )  # Result is the result of the called function, can be of any type.
    data = Signal(
        object
    )  # Partial in-progress result data (e.g. streaming data), can be of any type.


class WorkerBase(QRunnable):
    def __init__(self, *args, **kwargs):
        super(WorkerBase, self).__init__()
        # Generic worker base, including the standard signals and
        # error handling. Subclasses get this by default.
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.is_terminated = False

    @Slot()
    def run(self):
        try:
            result = self.do(
                *self.args, **self.kwargs
            )  # Subclasses implement their action on a do() method.
        except Exception as e:
            logging.error("Worker failed with exception %s", e)
            traceback.print_exc()
            self.signals.error.emit(e)
        else:
            logging.info("Worker complete with result %s", result)
            self.signals.complete.emit()
            self.signals.result.emit(result)

        self.signals.finished.emit()

    def do(self):
        raise NotImplementedError

    def terminate(self):
        # Set terminate flag (subclasses may not respect this).
        self.is_terminated = True
