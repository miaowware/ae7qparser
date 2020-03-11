"""
ae7q.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


from typing import Sequence

import requests
from bs4 import BeautifulSoup, element

from .base import *
from .tables import *
from .results import *


base_url = "http://ae7q.com/query/"

ca_pfx = ["va", "ve", "vo", "vy", "cy"]


##### PUBLIC FUNCTIONS
def get_call(callsign: str) -> Ae7qCallData:
    url = base_url + "data/CallHistory.php?CALL=" + callsign
    request = requests.get(url)

    html = request.text
    soup = BeautifulSoup(html, features="html.parser")

    tables = soup.find_all("table", "Database")

    processed_tables = _parse_tables(tables)

    parsed_tables = _assign_call_tables(processed_tables)

    if callsign[0:2] in ca_pfx:
        return Ae7qCanadianCallData(parsed_tables, callsign)
    else:
        return Ae7qCallData(parsed_tables, callsign)


def get_licensee_id(licensee_id: str) -> Ae7qLicenseeData:
    ...


def get_frn(frn: str) -> Ae7qFrnData:
    url = base_url + "data/FrnHistory.php?FRN=" + frn
    request = requests.get(url)

    html = request.text
    soup = BeautifulSoup(html, features="html.parser")

    tables = soup.find_all("table", "Database")

    processed_tables = _parse_tables(tables)

    parsed_tables = _assign_frn_tables(processed_tables)

    return Ae7qFrnData(parsed_tables, frn)


##### PRIVATE FUNCTIONS
def _parse_tables(tables: Sequence[element.Tag]) -> Sequence[Sequence[str]]:
    parsed_tables = []

    for table in tables:
        rows = table.find_all("tr")
        parsed_tables.append(__parse_table_rows(rows))

    return parsed_tables


def __parse_table_rows(table: Sequence[element.Tag]) -> Sequence[Sequence[str]]:
    rows = []
    remainder = []

    for tr in table:
        row = []
        next_remainder = []

        idx = 0
        for td in tr.find_all(["th", "td"]):
            # process rowspan > 1
            while remainder and remainder[0][0] <= idx:
                prev_idx, prev_cell, prev_rowspan = remainder.pop(0)
                row.append(prev_cell)
                if prev_rowspan > 1:
                    next_remainder.append((prev_idx, prev_cell, prev_rowspan - 1))
                idx += 1

            cell = __get_cell_text(td)
            try:
                rowspan = int(td.attrs["rowspan"])
            except (ValueError, KeyError): # catch %, attr not found
                rowspan = 1
            try:
                colspan = int(td.attrs["colspan"])
            except (ValueError, KeyError): # catch %, attr not found
                colspan = 1

            # handle colspan > 1
            for x in range(colspan):
                row.append(cell)
                if rowspan > 1:
                    next_remainder.append((idx, cell, rowspan - 1))
                idx += 1

            # get rid of ditto marks by copying the contents from the previous row
            for i, cell in enumerate(row):
                if cell == "\"":
                    row[i] = rows[-1][i]

        for prev_idx, prev_cell, prev_rowspan in remainder:
            row.append(prev_cell)
            if prev_rowspan > 1:
                next_remainder.append((prev_idx, prev_cell, prev_rowspan - 1))

        rows.append(row)
        remainder = next_remainder

    while remainder:
        next_remainder = []
        row = []

        for prev_idx, prev_cell, prev_rowspan in remainder:
            row.append(prev_cell)
            if rowspan > 1:
                next_remainder.append((prev_idx, prev_cell, prev_rowspan - 1))
        rows.append(row)
        remainder = next_remainder

    return rows


def __get_cell_text(cell: element.Tag) -> str:
    return " ".join(cell.getText().split())


def _assign_call_tables(tables: Sequence[Sequence]):
    out_tables = []
    for table in tables:
        # ConditionsTable
        if len(table) == 1 and len(table[0]) == 1:
            out_tables.append(ConditionsTable(table))

        # CallHistoryTable
        # Don't want the first row, it's a header
        elif len(table[0]) == 9 and table[0][0] == "Entity Name":
            out_tables.append(CallHistoryTable(table[1:]))

        # TrusteeTable
        elif len(table[0]) == 1 and len(table[1]) == 9 and table[1][0] == "Callsign":
            out_tables.append(TrusteeTable(table[2:]))

        # ApplicationsHistoryTable
        elif len(table[0]) == 9 and table[0][0] == "Receipt Date":
            out_tables.append(ApplicationsHistoryTable(table[1:]))

        # EventCallsignTable
        elif len(table[0]) == 5 and table[0][0] == "Start Date":
            out_tables.append(EventCallsignTable(table[1:]))

        # otherwise, Table
        else:
            out_tables.append(Table(table))

    return out_tables


def _assign_frn_tables(tables: Sequence[Sequence]):
    out_tables = []
    for table in tables:
        # FrnHistoryTable
        if len(table[0]) == 1 and len(table[1]) == 9 and table[1][0] == "Callsign":
            out_tables.append(FrnHistoryTable(table[2:]))

        # VanityApplicationsHistoryTable
        elif len(table[0]) >= 10 and table[0][0] == "Receipt Date":
            out_tables.append(VanityApplicationsHistoryTable(table[1:]))

        # otherwise, Table
        else:
            out_tables.append(Table(table))

    return out_tables
