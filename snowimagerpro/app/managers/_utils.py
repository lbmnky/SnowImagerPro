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

from collections import namedtuple
from collections.abc import Mapping
from typing import overload, Any, Optional


class BetterDict(Mapping):
    """
    Dictionary like object that allows for attribute access.

    Supports:
    - Key access: db_dict[key] -> value
    - Index access: db_dict[index] -> (key="key", value="value")
    - Slicing: db_dict[start:stop] -> dict

    Example: Linktable

    db_dict = DBDict(attrs=["uuid", "path"])

    db_dict["349432089"] = "path/to/db"
    db_dict["324092805"] = "path/to/db2"
    db_dict["490209503"] = "path/to/db3"
    db_dict["530948209"] = "path/to/db4"

    print(db_dict)
    >>> DBDict({'349432089': 'path/to/db', '324092805': 'path/to/db2'})

    print(db_dict["349432089"])
    >>> DBDictEntry(key='349432089', value='path/to/db')
    print(db_dict["349432089"].value)
    >>> 'path/to/db'

    print(db_dict[0])
    >>> DBDictEntry(key='349432089', value='path/to/db')
    print(db_dict[0].key)
    >>> '349432089'

    print(db_dict[0:2])
    >>> {'349432089': 'path/to/db', '324092805': 'path/to/db2'}

    """

    def __init__(self, *argv, attrs={"key": str, "value": str}, **karg):
        if len(attrs) != 2:
            raise ValueError("attrs must have exactly 2 keys")

        self._dict = dict(*argv, **karg)
        self._astuple = namedtuple("BetterDictEntry", attrs)

    @overload
    def __getitem__(self, key: Optional[int]) -> Any: ...

    @overload
    def __getitem__(self, key: slice) -> dict[str, str]: ...

    @overload
    def __getitem__(self, key: str) -> Any: ...

    def __getitem__(self, key: Optional[int] | slice | str):
        if isinstance(key, int):
            return self._iloc(key)
        if isinstance(key, slice):
            return self._islice(key)
        if isinstance(key, str):
            return self._astuple(key, self._dict[key])
        raise TypeError(f"Key must be either int, slice or str, not {type(key)}")

    def _iloc(self, index):
        _key = list(self._dict)[index]
        return self._astuple(_key, self._dict[_key])

    def _islice(self, slice):
        _keys = list(self._dict)[slice]
        return {key: self._dict[key] for key in _keys}

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        self._dict[key] = value
        self._update()

    def __delitem__(self, key):
        del self._dict[key]

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return (self._astuple(key, self._dict[key]) for key in self._dict)

    def __iter__(self):
        # return iter ... #TODO: Can I return a generator here?
        return (self._astuple(key, self._dict[key]) for key in self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return f"{type(self).__name__}({self._dict!r})"

    def as_dict(self):
        return self._dict

    def _update(self):
        print("BetterDict _dict has changed for databases ... TODO USE THIS!")
