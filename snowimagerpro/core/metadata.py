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

from ast import literal_eval
from pathlib import Path
from typing import List

from pydantic import BaseModel, ConfigDict, field_validator

DEFAULT_ROI = [
    [
        [[0.07691, 0.16448], [0.11837, 0.22293]],
        [[0.08479, 0.87572], [0.12991, 0.93579]],
        [[0.86776, 0.18187], [0.90737, 0.23641]],
    ],
    [
        [[0.07249, 0.2467], [0.11396, 0.30514]],
        [[0.08483, 0.9532], [0.12742, 0.99396]],
        [[0.8681, 0.26385], [0.90691, 0.31156]],
    ],
]

DEFAULT_coords_pix = [0.5, 0.5]
DEFAULT_coords_mm = [0.0, 0.0]


def stringCleaner(s_in: str) -> str:
    """Only keep characters necessary for nested lists of floats"""
    chars = set("0123456789.,[]-")
    s_out = "".join(c for c in s_in if c in chars)
    if len(s_out) != len(s_in.replace(" ", "")):
        raise ValueError("Invalid characters in string")
    return s_out


class ImageMetadata(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    filepath: Path = Path("")
    ID: int = 0
    img_type: str = "ngr"
    wavelength: float = 0.0
    drk_group: int = 0
    ref_group: int = 0
    meas_group: str = "0"
    location: str = "test"
    date: str = "2024-01-01"
    stack: str = "vert"
    ROI: List[List[List[List[float]]]] = DEFAULT_ROI
    coords_pix: List[float] = DEFAULT_coords_pix
    coords_mm: List[float] = DEFAULT_coords_mm
    px_2_mm: float = 1.0
    stitch_at_mm: List[float] = []
    affine_points: List[List[float]] = [[]]
    trafo_points: List[List[float]] = [[]]
    aux_data: str = "[]"
    comment: str = "_"

    def __setitem__(self, key, value):
        setattr(self, key, value)

    @field_validator(
        "ROI",
        "coords_pix",
        "coords_mm",
        "stitch_at_mm",
        "affine_points",
        "trafo_points",
        mode="before",
    )
    def validate_ROI(cls, v):
        if isinstance(v, list):
            return v
        return literal_eval(stringCleaner(v))

    def by_date(self):
        return self.date

    def by_location(self):
        return self.location

    def by_meas_group(self):
        return self.meas_group

    def by_img_type(self):
        return self.img_type

    def by_wavelength(self):
        return self.wavelength

    def by_ID(self):
        return self.ID

    def to_list(self):
        return [value for value in self.__dict__.values()]

    @classmethod
    def to_key_list(cls) -> List[str]:
        return list(cls.model_fields.keys())

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items()}

    def to_string(self):
        out = ""
        for key, value in self.__dict__.items():
            if key in ["ROI", "meas_group", "coords_pix", "coords_mm", "aux_data"]:
                out += f'"{value}",'
            else:
                out += f"{value},"

        return out[:-1]  # remove last comma

    def update(self, new_data):
        for key, value in new_data.items():
            setattr(self, key, str(value))


OutputDataSchema = {
    "type": "object",
    "properties": {
        "image": {
            "type": "array",
            "items": {"type": "array", "items": {"type": "number"}},
        },
        "pix2mm": {"type": "number"},
        "reference_pix_xz": {"type": "array", "items": {"type": "number"}},
        "reference_pos_xz": {"type": "array", "items": {"type": "number"}},
        "orig_image_metadata": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["image", "pix2mm", "reference_pix_xz", "reference_pos_xz"],
    "additionalProperties": False,
}


StitchedMetadataSchema = {
    "type": "object",
    "properties": {
        "coords_pix": {"type": "array", "items": {"type": "number"}},
        "coords_mm": {"type": "array", "items": {"type": "number"}},
    },
    "required": ["coords_pix", "coords_mm"],
    "additionalProperties": False,
}

StitchedMetadata: dict = {
    "wavelength": 0.0,
    "coords_pix": [0, 0],
    "coords_mm": [0, 0],
}
