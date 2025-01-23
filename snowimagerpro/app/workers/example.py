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

from workers.base import WorkerBase


class ExampleProcessor(WorkerBase):
    def do(self, images_to_process):
        """Proof of concept for background worker. Receives a list of
        images to process & emits a progress signal. You can build workers
        to perform any background tasks.

        """

        total_images = len(images_to_process)

        for n, image in enumerate(images_to_process):
            # Dummy process.
            time.sleep(0.25)
            # End dummy process.
            progress_pc = int(100 * (n / total_images))
            self.signals.progress.emit(progress_pc)

        self.signals.progress.emit(100)  # Complete.

        # You can return the resulting data at the end and it'll be emitted
        # on the result signal.
        return
