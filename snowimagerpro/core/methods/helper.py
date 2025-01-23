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

import json
import uuid
from ast import literal_eval
from copy import copy


def create_uuid() -> int:
    uid = uuid.uuid4().int & (1 << 32) - 1
    return round(uid, 8)


def logger(msg, end="\n"):
    print("\033[92m{}\033[0m".format("(logger)"), end=" ")
    print("\033[92m{}\033[0m".format(msg))


def warn(msg):
    print("\033[93m{}\033[0m".format("(warning)"), end=" ")
    print("\033[93m{}\033[0m".format(msg))


def debug(msg):
    print("\033[94m{}\033[0m".format("(debug)"), end=" ")
    print("\033[94m{}\033[0m".format(msg))


def error_msg(msg):
    print("\033[91m{}\033[0m".format("(error)"), end=" ")
    print("\033[91m{}\033[0m".format(msg))


def expand_db_by_meas_group(db):
    db_out = {}
    for key, entry in db.items():
        meas_grps = literal_eval(entry.meas_group)
        if isinstance(meas_grps, list):
            for meas_grp in meas_grps:
                entry.meas_group = str(meas_grp)
                new_key = create_uuid()
                entry.ID = new_key
                db_out[new_key] = copy(entry)
        else:
            db_out[key] = entry

    return db_out


def collapse_db(db):
    # TODO: This
    db_out = []
    [print(db[i].ID + " " + str(db[i].meas_group)) for i in range(len(db))]


def load_settings(settings_dir):
    return get_parameter_from_settings(settings_dir, None)


def get_parameter_from_settings(settings_dir, key):
    try:
        with open(
            settings_dir + "/snow_settings.json", "r", encoding="utf-8"
        ) as settings_file:
            settings = json.load(settings_file)
    except Exception:
        settings = None
        warn(
            "\n Please create a config.local file in the working directory with the "
            + "following entry: \n\n\tdata_dir: <standard/path/to/data/location/> \n\n This file "
            + "is ignored by git and can be used to set a default data location. \n"
        )

    if settings is not None:
        if key in settings.keys():
            return settings[key]
        elif key is None:
            return settings
        else:
            warn("key not found in settings file")
            return None


def bin_ndarray(ndarray, new_shape, operation="sum"):
    """
    https://gist.github.com/derricw/95eab740e1b08b78c03f


    Bins an ndarray in all axes based on the target shape, by summing or
        averaging.
    Number of output dimensions must match number of input dimensions.
    Example
    -------
    >>> m = np.arange(0,100,1).reshape((10,10))
    >>> n = bin_ndarray(m, new_shape=(5,5), operation='sum')
    >>> print(n)
    [[ 22  30  38  46  54]
     [102 110 118 126 134]
     [182 190 198 206 214]
     [262 270 278 286 294]
     [342 350 358 366 374]]
    """
    if operation.lower() not in ["sum", "mean", "average", "avg"]:
        raise ValueError("Operation {} not supported.".format(operation))
    if ndarray.ndim != len(new_shape):
        raise ValueError("Shape mismatch: {} -> {}".format(ndarray.shape, new_shape))
    compression_pairs = [(d, c // d) for d, c in zip(new_shape, ndarray.shape)]
    flattened = [l for p in compression_pairs for l in p]
    ndarray = ndarray.reshape(flattened)
    for i in range(len(new_shape)):
        if operation.lower() == "sum":
            ndarray = ndarray.sum(-1 * (i + 1))
        elif operation.lower() in ["mean", "average", "avg"]:
            ndarray = ndarray.mean(-1 * (i + 1))
    return ndarray
