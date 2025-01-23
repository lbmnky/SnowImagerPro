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

from pathlib import Path

from snowimagerpro.app.managers.jobs import threadpool
from snowimagerpro.app.managers.settings import user_config
from snowimagerpro.app.workers.run_func import ImageProcessor

from ..base import LogicBase
from .model import model
from .viewr import Viewr


def update_ui(func):
    def inner(self, *args):
        func(self, *args)
        model.signals.updated.emit()

    return inner


class Logic(LogicBase):
    def __init__(self):
        super().__init__()

        self.viewr = Viewr

    def post_init(self):
        self.initialize()

    @update_ui
    def initialize(self):
        model.post_init()

    @update_ui
    def update_model(self, idx, current_text):
        if not Path(current_text).is_dir():
            raise ValueError(f"The directory {current_text} does not exist.")

        model.private["currentDir"] = current_text

    @update_ui
    def add_default_dir(self, current_text):
        if not Path(current_text).is_dir():
            raise ValueError(f"The directory {current_text} does not exist.")

        if current_text not in model.private["defaultDirs"]:
            model.private["defaultDirs"] = model.private["defaultDirs"] + [current_text]
            user_config.set("inspector.defaultDirs", model.private["defaultDirs"])

    @update_ui
    def rmv_default_dir(self, current_text):
        if current_text in model.private["defaultDirs"]:
            idx = model.private["defaultDirs"].index(current_text)
            model.private["defaultDirs"].remove(current_text)
            model.private["currentDir"] = model.private["defaultDirs"][idx - 1]

    def load(self, fp):
        if not isinstance(fp, list):
            fp = Path(fp)

            def func():
                model.private["image"].load_from(fp)

            funcs = [func]
        else:
            fps = [Path(_fp) for _fp in fp]

            def func():
                model["image_set"].load_images(fps)

            funcs = [func]

        worker = ImageProcessor(funcs)

        worker.signals.progress.connect(self.progress)
        worker.signals.result.connect(self.show_raw_image)
        threadpool.start(worker)

    def normalize(self):
        # TODO: Implement stuff when more images loaded
        pass

    def show_raw_image(self):
        self.view(model.private["image"]._data)

    def view(self, img):
        view = self.viewr()
        view.setImage(img.T)
        view.closed.connect(self.remove_view)
        self.views = self.views + [view]
        view.show()


logic = Logic()
