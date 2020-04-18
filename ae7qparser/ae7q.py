"""
ae7q.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


from typing import Sequence, Union, List
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup, element

from .base import *
from .tables import *
from .results import *


base_url = "http://ae7q.com/query/"

ca_pfx = ["va", "ve", "vo", "vy", "cy"]


# ------ PUBLIC FUNCTIONS ------
def get_call(callsign: str) -> Union[Ae7qCallData, Ae7qCanadianCallData]:
    """
    Gets AE7Q data for a callsign. Works with American and Canadian calls.

    Args:
        callsign (str): Callsign to lookup.

    Returns:
        An Ae7qCallData or Ae7qCanadianCallData object.
    """
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
    """
    Gets AE7Q data for a Licensee ID.

    Args:
        licensee_id (str): Licensee ID to lookup.

    Returns:
        An Ae7qLicenseeData object.
    """
    url = base_url + "data/LicenseeIdHistory.php?ID=" + licensee_id
    request = requests.get(url)

    html = request.text
    soup = BeautifulSoup(html, features="html.parser")

    tables = soup.find_all("table", "Database")

    processed_tables = _parse_tables(tables)

    parsed_tables = _assign_licensee_tables(processed_tables)

    return Ae7qLicenseeData(parsed_tables, licensee_id)


def get_frn(frn: str) -> Ae7qFrnData:
    """
    Gets AE7Q data for an FRN.

    Args:
        frn (str): FRN to lookup.

    Returns:
        An Ae7qFrnData object.
    """
    url = base_url + "data/FrnHistory.php?FRN=" + frn
    request = requests.get(url)

    html = request.text
    soup = BeautifulSoup(html, features="html.parser")

    tables = soup.find_all("table", "Database")

    processed_tables = _parse_tables(tables)

    parsed_tables = _assign_frn_tables(processed_tables)

    return Ae7qFrnData(parsed_tables, frn)


def get_application(app_id: str) -> Ae7qApplicationData:
    """
    Gets AE7Q data for a ULS File Number.

    Args:
        app_id (str): UFN to lookup.

    Returns:
        An Ae7qApplicationData object.
    """
    url = base_url + "data/AppDetail.php?UFN=" + app_id
    request = requests.get(url)

    html = request.text
    soup = BeautifulSoup(html, features="html.parser")

    tables = soup.find_all("table", "Database")

    processed_tables = _parse_tables(tables)
    parsed_tables = []

    for table in processed_tables:
        if table[0][0] == "Field Name":
            table[1][1] = "Data"
            parsed_tables.append(Table(table, 1))
        elif table[0][0] == "Action Date":
            parsed_tables.append(ApplicationActionHistoryTable(table))
        elif table[0][0] == "Attachment records":
            parsed_tables.append(ApplicationAttachmentsTable(table, 1))
        elif table[0][1] == "Vanity Callsign":
            parsed_tables.append(ApplicationVanityCallsignsTable(table))
        else:
            parsed_tables.append(Table(table))

    return Ae7qApplicationData(parsed_tables, app_id)


# ------ PRIVATE FUNCTIONS ------
def _parse_tables(tables: Sequence[element.Tag]) -> List[List[List[Union[str, datetime]]]]:
    # converts a list of html tables to a list of lists of text or datetimes
    parsed_tables = []

    for table in tables:
        rows = table.find_all("tr")
        parsed_tables.append(__parse_table_rows(rows))

    return parsed_tables


def __parse_table_rows(table: Sequence[element.Tag]) -> List[List[Union[str, datetime]]]:
    # converts a table into rows of text or datetime
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
            except (ValueError, KeyError):  # catch %, attr not found
                rowspan = 1
            try:
                colspan = int(td.attrs["colspan"])
            except (ValueError, KeyError):  # catch %, attr not found
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

    if rows[0][-1] == "Vanity callsign(s) applied for":
        # combine application rows and applied callsigns
        new_rows = []
        for row in rows:
            if row[4] not in [x[4] for x in new_rows]:
                matching_rows = [x for x in rows if x[4] == row[4]]
                new_row = row[0:9]
                new_cell = []
                for r in matching_rows:
                    new_cell += [x for x in r[9:] if x != ""]
                new_row.append(tuple(new_cell))
                new_rows.append(new_row)
        new_rows[0][-1] = "Vanity callsign(s) applied for"
        return new_rows

    return rows


def __get_cell_text(cell: element.Tag) -> Union[str, datetime]:
    # gets the (better-formatted) cell text. If in certain formats, it will convert to datetime.
    text = " ".join(cell.stripped_strings)
    if re.fullmatch(r"\w{3} \d{4}-\d{2}-\d{2}", text):
        text = datetime.strptime(text, "%a %Y-%m-%d")
    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        text = datetime.strptime(text, "%Y-%m-%d")
    elif re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", text):
        text = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
    elif text == r"(none)":
        text = ""
    return text


def _assign_call_tables(tables: List[List[List]]):
    # create Table objects for a callsign query
    out_tables = []
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

        # ApplicationsHistoryTable
        elif len(table[0]) == 9 and table[0][0] == "Receipt Date":
            out_tables.append(ApplicationsHistoryTable(table))

        # EventCallsignTable
        elif len(table[0]) == 5 and table[0][0] == "Start Date":
            out_tables.append(EventCallsignTable(table))

        # PendingApplicationsPredictionsTable
        elif len(table[0]) == 10 and table[0][-1] == "Prediction":
            out_tables.append(CallsignPendingApplicationsPredictionsTable(table))

        # otherwise, Table
        else:
            out_tables.append(Table(table, -1))

    return out_tables


def _assign_licensee_tables(tables: List[List[List]]):
    # create Table objects for a licensee ID query
    out_tables = []
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


def _assign_frn_tables(tables: List[List[List]]):
    # create Table objects for an FRN query
    out_tables = []
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
