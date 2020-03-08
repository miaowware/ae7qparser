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

    tables = [table for table in soup.select("table.Database")]

    processed_tables = __process_tables(tables)

    parsed_tables = __parse_tables(processed_tables)

    if callsign[0:2] in ca_pfx:
        return Ae7qCanadianCallData(parsed_tables, callsign)
    else:
        return Ae7qCallData(parsed_tables, callsign)


def get_licensee_id(licensee_id: str) -> Ae7qLicenseeData:
    ...


def get_frn(frn: str) -> Ae7qFrnData:
    ...


##### PRIVATE FUNCTIONS
def __process_tables(tables: Sequence[element.Tag]) -> Sequence[Sequence]:
    parsed_tables = []
    for table in tables:
        parsed_table = []
        rows = [row for row in table.find_all("tr")]
        for tr in rows:
            row = []
            for cell in tr.find_all(["th", "td"]):
                cell_val = " ".join(cell.getText().split())
                row.append(cell_val if cell_val else None)

                # separate combined columns
                if "colspan" in cell.attrs:
                    try:
                        if int(cell.attrs["colspan"]) > 1:
                            for i in range(int(cell.attrs["colspan"]) - 1):
                                row.append(row[-1])
                    except ValueError:
                        pass

            # get rid of ditto marks by copying the contents from the previous row
            for i, cell in enumerate(row):
                if cell == "\"":
                    row[i] = parsed_table[-1][i]
            # add row to table
            parsed_table += [row]
        parsed_tables.append(parsed_table)

    return parsed_tables


def __parse_tables(tables: Sequence[Sequence]):
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
