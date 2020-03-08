"""
base.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


from typing import Sequence


class Row:
    def __init__(self, row_data: Sequence):
        self.data = row_data

    def __str__(self):
        return ";".join([str(cell) for cell in self.data])


class Table:
    row_cls = Row  # Class attribute
    def __init__(self, data: Sequence[Sequence]):
        rows = []
        for row_data in data:
            rows.append(self.row_cls(row_data))
        self.rows = tuple(rows)  # Making the data immutable

    def __str__(self):
        return "\n".join([str(row) for row in self.rows])


class Ae7qData:
    def __init__(self, tables: Sequence[Table], query: str, query_url: str):
        self.tables = tables
        self.query = query
        self.query_url = query_url

    def __repr__(self):
        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__
        return f"<{module}.{qualname} object with query {self.query}>"

    def __str__(self):
        out = f"Query: {self.query}\n"
        out += f"Query URL: {self.query_url}\n\n"
        for table in self.tables:
            cls_name = type(table).__name__
            out += f"{cls_name}:\n{table}\n\n"
        return out
