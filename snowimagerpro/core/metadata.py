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
from typing import List, Any

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

DEFAULT_ROI_TOP = [
    [
        [
            [0.055922165406118406, 0.43246892777982116],
            [0.09557393510117622, 0.4936438970278278],
        ],
        [
            [0.054920512769758255, 0.6066541129601855],
            [0.09442099989433937, 0.6659040648092227],
        ],
        [
            [0.9115949694981781, 0.43635504933727454],
            [0.952665085439197, 0.4991744830844058],
        ],
        [
            [0.9101967893557827, 0.608686155165703],
            [0.9505750590544825, 0.6672196684083709],
        ],
    ],
    [
        [
            [0.05729923563713338, 0.35152301730534624],
            [0.09334271169654294, 0.4080654331351102],
        ],
        [
            [0.056643316033994716, 0.5191269896828924],
            [0.09596166927073194, 0.5793022031679653],
        ],
        [
            [0.9101452303790001, 0.3481500983092285],
            [0.9493202593642547, 0.40998383823080553],
        ],
        [
            [0.9110023647757527, 0.5231540074833108],
            [0.9499449814404536, 0.5841226482986643],
        ],
    ],
]

DEFAULT_ROI_BOTTOM = [
    [
        [
            [0.05405438515543442, 0.4595033254380134],
            [0.09124228830832154, 0.5158500211720395],
        ],
        [
            [0.05143016095876016, 0.6256962321247685],
            [0.09273555713758438, 0.6839932674814768],
        ],
        [
            [0.9079156310593696, 0.4709599357206003],
            [0.9475256310593697, 0.5254999357206003],
        ],
        [
            [0.9041780072157628, 0.6378247415220349],
            [0.9449213058997172, 0.6952105723204809],
        ],
    ],
    [
        [
            [0.05315386434907439, 0.3785613327580951],
            [0.08904333735573078, 0.42976184595922706],
        ],
        [
            [0.051835518318843296, 0.5450410613872856],
            [0.0903515584663348, 0.594836929498675],
        ],
        [
            [0.9067930686702421, 0.3825067515829073],
            [0.9440156121960526, 0.44010075689325623],
        ],
        [
            [0.9068465798172102, 0.556486106850577],
            [0.9443290805408925, 0.6103419357524696],
        ],
    ],
]

DEFAULT_ROI_REF = [
    [
        [
            [0.17594055040394674, 0.19132321504463634],
            [0.8187736643429468, 0.8014233363704985],
        ]
    ],
    [],
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
    exif: Any = {}
    meta: Any = {}

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

    def by_drk_group(self):
        return self.drk_group

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
    "date": "2000-01-01",
    "location": "",
}
