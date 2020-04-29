"""
dummy.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


from typing import Union

from .results import (
    Ae7qCallData,
    Ae7qCanadianCallData,
    Ae7qLicenseeData,
    Ae7qFrnData,
    Ae7qApplicationData,
)


def get_call(callsign: str) -> Union[Ae7qCallData, Ae7qCanadianCallData]:
    raise NotImplementedError("You must install the package requests to use this function.")


def get_licensee_id(licensee_id: str) -> Ae7qLicenseeData:
    raise NotImplementedError("You must install the package requests to use this function.")


def get_frn(frn: str) -> Ae7qFrnData:
    raise NotImplementedError("You must install the package requests to use this function.")


def get_application(app_id: str) -> Ae7qApplicationData:
    raise NotImplementedError("You must install the package requests to use this function.")


def a_get_call(callsign: str) -> Union[Ae7qCallData, Ae7qCanadianCallData]:
    raise NotImplementedError("You must install the package aiohttp to use this function.")


def a_get_licensee_id(licensee_id: str) -> Ae7qLicenseeData:
    raise NotImplementedError("You must install the package aiohttp to use this function.")


def a_get_frn(frn: str) -> Ae7qFrnData:
    raise NotImplementedError("You must install the package aiohttp to use this function.")


def a_get_application(app_id: str) -> Ae7qApplicationData:
    raise NotImplementedError("You must install the package aiohttp to use this function.")
