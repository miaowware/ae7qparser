"""
parse.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


from typing import Sequence, Union, List, Tuple
import re
from datetime import datetime

from bs4 import element

from .tables import (
    Table,
    ConditionsTable,
    CallHistoryTable,
    TrusteeTable,
    ApplicationsHistoryTable,
    VanityApplicationsHistoryTable,
    PendingApplicationsPredictionsTable,
    CallsignPendingApplicationsPredictionsTable,
    EventCallsignTable,
    FrnHistoryTable,
    LicenseeIdHistoryTable,
    ApplicationActionHistoryTable,
    ApplicationVanityCallsignsTable,
    ApplicationAttachmentsTable,
)


__all__ = [
    "_parse_tables",
    "_assign_call_tables",
    "_assign_frn_tables",
    "_assign_licensee_tables",
    "_assign_application_tables",
]


def _parse_tables(tables: Sequence[element.Tag]) -> List[List[List[Union[str, datetime]]]]:
    # converts a list of html tables to a list of lists of text or datetimes
    parsed_tables = []

    for table in tables:
        rows = table.find_all("tr")
        parsed_tables.append(_parse_table_rows(rows))

    return parsed_tables


def _parse_table_rows(table: Sequence[element.Tag]) -> List[List[Union[str, datetime]]]:
    # converts a table into rows of text or datetime
    rows = []

    for tr in table:
        raw_row = []

        for td in tr.find_all(["th", "td"]):
            try:
                rowspan = int(td.attrs.get("rowspan", 1))
            except ValueError:  # catch %
                rowspan = -1
            try:
                colspan = int(td.attrs.get("colspan",1))
            except ValueError:  # catch %
                colspan = -1

            cell = _get_cell_text(td)
            raw_row.append((cell, rowspan, colspan))

            # if colspan == -1:
            #     row = [cell]

            # # handle colspan > 1
            # for x in range(colspan):
            #     row.append(cell)
            #     if rowspan > 1:
            #         next_remainder.append((idx, cell, rowspan - 1))
            #     idx += 1

        print(raw_row)
        # get rid of ditto marks by copying the contents from the previous row
        # for i, cell in enumerate(raw_row):
        #     if cell[0] == "\"":
        #         raw_row[i] = (rows[-1][i][0], cell[1], cell[2])

        rows.append(raw_row)

        # for prev_idx, prev_cell, prev_rowspan in remainder:
        #     row.append(prev_cell)
        #     if prev_rowspan > 1:
        #         next_remainder.append((prev_idx, prev_cell, prev_rowspan - 1))

        # rows.append(row)
        # remainder = next_remainder

    # while remainder:
        # next_remainder = []
        # row = []

        # for prev_idx, prev_cell, prev_rowspan in remainder:
        #     row.append(prev_cell)
        #     if rowspan > 1:
        #         next_remainder.append((prev_idx, prev_cell, prev_rowspan - 1))
        # rows.append(row)
        # remainder = next_remainder

    if rows[0][-1] == "Vanity callsign(s) applied for":
        # combine application rows and applied callsigns
        new_rows = []
        for row in rows:                                                # take all rows in the table
            if row[4] not in [x[4] for x in new_rows]:                  # if the UFN isn't already in the new table
                matching_rows = [x for x in rows if x[4] == row[4]]     # find all rows for that UFN
                new_row = row[0:9]                                      # take all cells of the row except the last col
                new_cell = []

                for r in matching_rows:                                 # for reach row with that UFN,
                    new_cell += [x for x in r[9:] if x != ""]           # add each callsign to the new cell (if not "")
                new_row.append(tuple(new_cell))                         # convert the cell to a tuple and append to new row
                new_rows.append(new_row)                                # add new row to new table
        new_rows[0][-1] = "Vanity callsign(s) applied for"              # add the last column title
        return new_rows

    return rows


def _get_cell_text(cell: element.Tag) -> Union[str, datetime]:
    # gets the (better-formatted) cell text. If in certain formats, it will convert to datetime.
    text = " ".join([" ".join(x.split()) for x in cell.stripped_strings])
    out: Union[str, datetime]

    if re.fullmatch(r"\w{3} \d{4}-\d{2}-\d{2}", text):
        out = datetime.strptime(text, "%a %Y-%m-%d")
    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        out = datetime.strptime(text, "%Y-%m-%d")
    elif re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", text):
        out = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")

    elif text == r"(none)":
        out = ""
    else:
        out = text

    return out


def _assign_call_tables(tables: List[List[List]]) -> List[Table]:
    # create Table objects for a callsign query
    out_tables: List[Table] = []
    for table in tables:
        # ConditionsTable
        if len(table) == 1 and len(table[0]) == 1:
            out_tables.append(ConditionsTable(table, -1))

        # CallHistoryTable
        # Don't want the first row, it's a header
        elif len(table[0]) == 9 and table[0][0] == "Entity Name":
            out_tables.append(CallHistoryTable(table))

        # TrusteeTable
        elif len(table[0]) == 1 and len(table[1]) == 9 and table[1][0] == "Callsign":
            out_tables.append(TrusteeTable(table, 1))

        # CallsignPendingApplicationsPredictionsTable
        elif table[0][-1] == "Prediction":
            out_tables.append(CallsignPendingApplicationsPredictionsTable(table))

        # ApplicationsHistoryTable
        elif len(table[0]) == 9 and table[0][0] == "Receipt Date":
            out_tables.append(ApplicationsHistoryTable(table))

        # EventCallsignTable
        elif len(table[0]) == 5 and table[0][0] == "Start Date":
            out_tables.append(EventCallsignTable(table))

        # otherwise, Table
        else:
            out_tables.append(Table(table, -1))

    return out_tables


def _assign_licensee_tables(tables: List[List[List]]) -> List[Table]:
    # create Table objects for a licensee ID query
    out_tables: List[Table] = []
    for table in tables:
        # LicenseeIdHistoryTable
        if len(table[0]) == 1 and len(table[1]) == 10 and table[1][0] == "Callsign":
            out_tables.append(LicenseeIdHistoryTable(table, 1))

        # PendingApplicationsPredictionsTable
        elif len(table[0]) == 10 and table[0][-1] == "Prediction":
            out_tables.append(PendingApplicationsPredictionsTable(table))

        # VanityApplicationsHistoryTable
        elif len(table[0]) == 10 and table[0][0] == "Receipt Date":
            out_tables.append(VanityApplicationsHistoryTable(table))

        # otherwise, Table
        else:
            out_tables.append(Table(table, -1))

    return out_tables


def _assign_frn_tables(tables: List[List[List]]) -> List[Table]:
    # create Table objects for an FRN query
    out_tables: List[Table] = []
    for table in tables:
        # FrnHistoryTable
        if len(table[0]) == 1 and len(table[1]) == 10 and table[1][0] == "Callsign":
            out_tables.append(FrnHistoryTable(table, 1))

        # PendingApplicationsPredictionsTable
        elif len(table[0]) == 10 and table[0][-1] == "Prediction":
            out_tables.append(PendingApplicationsPredictionsTable(table))

        # VanityApplicationsHistoryTable
        elif len(table[0]) == 10 and table[0][0] == "Receipt Date":
            out_tables.append(VanityApplicationsHistoryTable(table))

        # otherwise, Table
        else:
            out_tables.append(Table(table, -1))

    return out_tables


def _assign_application_tables(tables: List[List[List]]) -> List[Table]:
    # create Table objects for an application query
    out_tables: List[Table] = []
    for table in tables:
        # application data
        if table[0][0] == "Field Name":
            table[1][1] = "Data"
            out_tables.append(Table(table, 1))
        # action history
        elif table[0][0] == "Action Date":
            out_tables.append(ApplicationActionHistoryTable(table))
        # attachments
        elif table[0][0] == "Attachment records":
            out_tables.append(ApplicationAttachmentsTable(table, 1))
        # vanity calls
        elif table[0][1] == "Vanity Callsign":
            out_tables.append(ApplicationVanityCallsignsTable(table))
        else:
            out_tables.append(Table(table))
    return out_tables
