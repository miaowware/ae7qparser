"""
tables.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


import collections.abc as abc
from typing import Sequence, Union


from .rows import (
    Row,
    ConditionsRow,
    CallHistoryRow,
    TrusteeRow,
    ApplicationsHistoryRow,
    VanityApplicationsHistoryRow,
    PendingApplicationsPredictionsRow,
    CallsignPendingApplicationsPredictionsRow,
    EventCallsignRow,
    FrnHistoryRow,
    LicenseeIdHistoryRow,
    ApplicationActionHistoryRow,
    ApplicationVanityCallsignsRow,
    ApplicationAttachmentsRow,
)


__all__ = [
    "Table",
    "ConditionsTable",
    "CallHistoryTable",
    "TrusteeTable",
    "ApplicationsHistoryTable",
    "VanityApplicationsHistoryTable",
    "PendingApplicationsPredictionsTable",
    "CallsignPendingApplicationsPredictionsTable",
    "EventCallsignTable",
    "FrnHistoryTable",
    "LicenseeIdHistoryTable",
    "ApplicationActionHistoryTable",
    "ApplicationVanityCallsignsTable",
    "ApplicationAttachmentsTable",
]


class Table(abc.Sequence):
    """Class representing a table of ae7q data. The table's data can be accessed like a sequence.

    :param data: the data to be stored in the table.
    :type data: Sequence[Sequence]
    :param header_row: the row to use as column names. Defaults to first row. If -1, no row will be used.
    :type header_row: int, Optional

    :var col_names: the names of each column in the table.
    :vartype col_names: :class:`ae7qparser.rows.Row`, None
    """
    _row_cls = Row  # Class attribute of rows contained by this class.

    def __init__(self, data: Sequence[Sequence], header_row: int = 0):
        if header_row == -1:
            self.col_names = None
        else:
            self.col_names = Row(data[header_row])
        header_row += 1

        rows = []
        for row_data in data[header_row:]:
            rows.append(self._row_cls(row_data))
        self._data = tuple(rows)  # Making the data immutable

    @property
    def csv(self) -> str:
        """Returns each row's data separated by semicolons, with each row separated by a newline, including column names."""
        csv = self.col_names.csv + "\n" if self.col_names is not None else ""
        csv += "\n".join([row.csv for row in self._data])
        return csv

    @property
    def csv_pretty(self) -> str:
        """Returns each row's data, separated by pipes, with each row separated by a newline, including column names."""
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

    def __getitem__(self, index: Union[int, slice]):
        return self._data[index]

    def __iter__(self):
        return iter(self._data)


class ConditionsTable(Table):
    """Class representing a table of license or callsign conditions."""
    _row_cls = ConditionsRow  # Class attribute


class CallHistoryTable(Table):
    """Class representing a table of callsign history."""
    _row_cls = CallHistoryRow


class TrusteeTable(Table):
    """Class representing a table of trustee history."""
    _row_cls = TrusteeRow


class ApplicationsHistoryTable(Table):
    """Class representing a table of applications history."""
    _row_cls = ApplicationsHistoryRow


class VanityApplicationsHistoryTable(Table):
    """Class representing a table of applications history with vanity callsigns listed."""
    _row_cls = VanityApplicationsHistoryRow


class PendingApplicationsPredictionsTable(Table):
    """Class representing a table of pending applications with predictions."""
    _row_cls = PendingApplicationsPredictionsRow


class CallsignPendingApplicationsPredictionsTable(Table):
    """Class representing a table of pending applications with predictions (on a callsign query)."""
    _row_cls = CallsignPendingApplicationsPredictionsRow


class EventCallsignTable(Table):
    """Class representing a table of special event callsign history."""
    _row_cls = EventCallsignRow


class FrnHistoryTable(Table):
    """Class representing a table of FRN history."""
    _row_cls = FrnHistoryRow


class LicenseeIdHistoryTable(Table):
    """Class representing a table of Licensee ID history."""
    _row_cls = LicenseeIdHistoryRow


class ApplicationActionHistoryTable(Table):
    """Class representing a table of an application's action history."""
    _row_cls = ApplicationActionHistoryRow


class ApplicationVanityCallsignsTable(Table):
    """Class representing a table of an application's vanity callsigns."""
    _row_cls = ApplicationVanityCallsignsRow


class ApplicationAttachmentsTable(Table):
    """Class representing a table of an application's attachments."""
    _row_cls = ApplicationAttachmentsRow
