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

import time

from snowimagerpro.app.workers.base import WorkerBase


class ImageProcessor(WorkerBase):
    def do(self, func):
        """Proof of concept to run function on set of images."""
        self.signals.progress.emit(0)

        N = len(func)

        images_processed = []

        for n, f in enumerate(func):
            # Dummy process.
            #time.sleep(0.75)
            #out = func(image)
            #out = func(_in)
            out = f()
            #out = None
            images_processed.append(out)
            # End dummy process.
            progress_pc = int(100 * ((n+1) / (N - 0)))
            self.signals.progress.emit(progress_pc)

        # You can return the resulting data at the end and it'll be emitted
        # on the result signal.
        return images_processed
