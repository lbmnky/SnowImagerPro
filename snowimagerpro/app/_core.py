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

# This is a patch to snowimagerpro/core to add signals to the Image, ImageSet,
# and ImageForAnalysis classes.

import time

from PySide6.QtCore import QObject, Signal

import snowimagerpro.core as sipro_core
from snowimagerpro.app.managers.jobs import threadpool
from snowimagerpro.app.workers.run_func import ImageProcessor


def signalling_progress(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.sig_progress.emit(self.total_progress)
        self.sig_status.emit(self.status_msg)

        if self.total_progress >= 99:

            def reset_progress():
                time.sleep(1.5)
                self.sig_progress.emit(-1)
                self.sig_status.emit("")

            worker = ImageProcessor([reset_progress])
            worker.setAutoDelete(True)
            threadpool.start(worker)

    return wrapper


class Image(QObject, sipro_core.Image):
    def __init__(self) -> None:
        super(Image, self).__init__()


class ImageSet(QObject, sipro_core.ImageSet):
    """Redefine ImagerSet from snowimagerpro/core to add signals."""

    sig_progress = Signal(int)
    sig_status = Signal(str)

    def __init__(self) -> None:
        super(ImageSet, self).__init__()

    inc_progress_by = signalling_progress(sipro_core.ImageSet.inc_progress_by)


class ImageForAnalysis(QObject, sipro_core.ImageForAnalysis):
    def __init__(self) -> None:
        super(ImageForAnalysis, self).__init__()
