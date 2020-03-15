"""
base.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""

import json
import collections.abc as abc
from datetime import datetime
from typing import Sequence


class Row(abc.Sequence):
    def __init__(self, row_data: Sequence):
        self._data = tuple(row_data)

    @property
    def csv(self) -> str:
        csv_data = []
        for cell in self._data:
            if isinstance(cell, list) or isinstance(cell, tuple):
                cell = ",".join(cell)
            csv_data.append(cell)
        return ";".join([str(cell) for cell in csv_data])

    # --- Wrappers to implement sequence-like functionality ---
    def __len__(self):
        return len(self._data)

    def __getitem__(self, index: int):
        return self._data[index]

    def __iter__(self):
        return iter(self._data)

    # ---
    def __str__(self):
        return str(self._data)


class Table(abc.Sequence):
    row_cls = Row  # Class attribute
    def __init__(self, data: Sequence[Sequence]):
        rows = []
        for row_data in data:
            rows.append(self.row_cls(row_data))
        self._data = tuple(rows)  # Making the data immutable

    @property
    def csv(self) -> str:
        return "\n".join([row.csv for row in self._data])

    # --- Wrappers to implement sequence-like functionality ---
    def __len__(self):
        return len(self._data)

    def __getitem__(self, index: int):
        return self._data[index]

    def __iter__(self):
        return iter(self._data)

    # ---
    def __str__(self):
        return str(tuple([str(row) for row in self._data]))


class Ae7qData:
    def __init__(self, tables: Sequence[Table], query: str, query_url: str):
        self.tables = tuple(tables)
        self.query = query
        self.query_url = query_url
        self.query_time = datetime.utcnow()

    def __repr__(self):
        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__
        return (f"<{module}.{qualname} object at {hex(id(self))}, "
                f"query={self.query}>")
