"""
sync.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


from typing import Union

import requests
from bs4 import BeautifulSoup

from .results import (
    Ae7qCallData,
    Ae7qCanadianCallData,
    Ae7qLicenseeData,
    Ae7qFrnData,
    Ae7qApplicationData,
)
from .utils import base_url, ca_pfx
from .parse import (
    _parse_tables,
    _assign_call_tables,
    _assign_frn_tables,
    _assign_licensee_tables,
    _assign_application_tables,
)


__all__ = [
    "get_call",
    "get_frn",
    "get_licensee_id",
    "get_application",
]


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

    if callsign[0:2].lower() in ca_pfx:
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
    parsed_tables = _assign_application_tables(processed_tables)

    return Ae7qApplicationData(parsed_tables, app_id)
