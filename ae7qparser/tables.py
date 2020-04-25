"""
tables.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


import collections.abc as abc
from typing import Sequence


class Table(abc.Sequence):
    """Table
    ------

    Class representing a Table.
    Initialised with a nested sequence and (optionally) a row to use as column headers.

    The table's data can be accessed like a sequence.

    Args:
        data (Sequence[Sequence]): the data to be stored in the Table.
        header_row (int): the row to store as column names. If not provided, the first row will be used. If -1, no row
            will be used as column names.

    Attributes:
        col_names (Sequence): the names of each column in the table.
        row_cls (Row): the class to use for the Table's rows. By default, the class is Row.

    Properties:
        csv (str): returns each row's data separated by semicolons, with each row separated by a newline. It includes
            column names.
        csv_pretty (str): returns each row's data, separated by pipes, with each row separated by a newline. It includes
            column names.
    """
    row_cls = Row  # Class attribute

    def __init__(self, data: Sequence[Sequence], header_row: int = 0):
        if header_row == -1:
            self.col_names = None
        else:
            self.col_names = Row(data[header_row])
        header_row += 1

        rows = []
        for row_data in data[header_row:]:
            rows.append(self.row_cls(row_data))
        self._data = tuple(rows)  # Making the data immutable

    @property
    def csv(self) -> str:
        csv = self.col_names.csv + "\n" if self.col_names is not None else ""
        csv += "\n".join([row.csv for row in self._data])
        return csv

    @property
    def csv_pretty(self) -> str:
        csv_out = ""
        csv = [self.col_names.csv.split(";")] if self.col_names is not None else []
        csv += [row.csv.split(";") for row in self._data]
        maxes = []
        for i in range(0, len(csv[-1])):
            maxes.append(max([len(str(x[i])) for x in csv]))

        for i, row in enumerate(csv):
            for j in range(0, len(csv[0])):
                csv_out += f"{row[j]:<{maxes[j]}}"
                if j != len(csv[0]) - 1:
                    csv_out += " | "
            if i != len(csv) - 1:
                csv_out += "\n"

        return csv_out

    def __str__(self):
        return str(tuple([str(row) for row in self._data]))

    # --- Wrappers to implement sequence-like functionality ---
    def __len__(self):
        return len(self._data)

    def __getitem__(self, index: int):
        return self._data[index]

    def __iter__(self):
        return iter(self._data)


class ConditionsTable(Table):
    row_cls = ConditionsRow  # Class attribute


class CallHistoryTable(Table):
    row_cls = CallHistoryRow


class TrusteeTable(Table):
    row_cls = TrusteeRow


class ApplicationsHistoryTable(Table):
    row_cls = ApplicationsHistoryRow


class VanityApplicationsHistoryTable(Table):
    row_cls = VanityApplicationsHistoryRow


class PendingApplicationsPredictionsTable(Table):
    row_cls = PendingApplicationsPredictionsRow


class CallsignPendingApplicationsPredictionsTable(Table):
    row_cls = CallsignPendingApplicationsPredictionsRow


class EventCallsignTable(Table):
    row_cls = EventCallsignRow


class FrnHistoryTable(Table):
    row_cls = FrnHistoryRow


class LicenseeIdHistoryTable(Table):
    row_cls = LicenseeIdHistoryRow


class ApplicationActionHistoryTable(Table):
    row_cls = ApplicationActionHistoryRow


class ApplicationVanityCallsignsTable(Table):
    row_cls = ApplicationVanityCallsignsRow


class ApplicationAttachmentsTable(Table):
    row_cls = ApplicationAttachmentsRow
