"""
results.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


from typing import Sequence

from .base import *
from .tables import *


base_url = "http://ae7q.com/query/"


class Ae7qCallData(Ae7qData):
    # http://ae7q.com/query/data/CallHistory.php?CALL=kn8u
    def __init__(self, tables: Sequence[Table], query: str):
        url = base_url + "data/CallHistory.php?CALL=" + query
        super().__init__(tables, query, url)

        self.conditions = None
        self.call_history = None
        self.trustee_history = None
        self.application_history = None

        for table in tables:
            if self.conditions is None and isinstance(table, ConditionsTable):
                self.conditions = table
            elif self.call_history is None and isinstance(table, CallHistoryTable):
                self.call_history = table
            elif self.trustee_history is None and isinstance(table, TrusteeTable):
                self.trustee_history = table
            elif self.application_history is None and isinstance(table, ApplicationsHistoryTable):
                self.application_history = table


class Ae7qCanadianCallData(Ae7qData):
    # http://ae7q.com/query/data/CallHistory.php?CALL=va2shf
    def __init__(self, tables: Sequence[Table], query: str):
        url = base_url + "data/FrnHistory.php?FRN=" + query
        super().__init__(tables, query, url)

        data = tables[0]

        self.callsign = None
        self.given_names = None
        self.surname = None
        self.address = None
        self.locality = None
        self.province = None
        self.postal_code = None
        self.country = None
        self.region = None
        self.grid_square = None
        self.qualifications = None

        for row in data[1:]:
            if self.callsign is None and row[0] == "Callsign":
                self.callsign = row[1]
            elif self.given_names is None and row[0] == "Given Names":
                self.given_names = row[1]
            elif self.surname is None and row[0] == "Surname":
                self.surname = row[1]
            elif self.address is None and row[0] == "Street Address":
                self.address = row[1]
            elif self.locality is None and row[0] == "Locality":
                self.locality = row[1]
            elif self.province is None and row[0] == "Province":
                self.province = row[1]
            elif self.postal_code is None and row[0] == "Postal Code":
                self.postal_code = row[1]
            elif self.country is None and row[0] == "Country":
                self.country = row[1]
            elif self.region is None and row[0] == "Region":
                self.region = row[1]
            elif self.grid_square is None and row[0] == "Maidenhead":
                self.grid_square = row[1]
            elif self.qualifications is None and row[0] == "Qualifications":
                self.qualifications = row[1]

class Ae7qLicenseeData(Ae7qData):
    # http://ae7q.com/query/data/LicenseeIdHistory.php?ID=L01295086
    pass


class Ae7qFrnData(Ae7qData):
    # http://ae7q.com/query/data/FrnHistory.php?FRN=0016605636
    def __init__(self, tables: Sequence[Table], query: str):
        url = base_url + "data/FrnHistory.php?FRN=" + query
        super().__init__(tables, query, url)

        self.frn_history = None
        self.application_history = None

        for table in tables:
            if self.frn_history is None and isinstance(table, FrnHistoryTable):
                self.frn_history = table
            elif self.application_history is None and isinstance(table, VanityApplicationsHistoryTable):
                self.application_history = table


class Ae7qApplicationData(Ae7qData):
    # http://ae7q.com/query/data/AppDetail.php?UFN=0008963527
    pass

# other queries:
# maybe for future?
# http://ae7q.com/query/list/AppByReceipt.php?DATE=2018-06-08
# http://www.ae7q.com/query/list/ProcessDate.php?DATE=yesterday
# http://www.ae7q.com/query/list/CallByZip.php?ZIP5=07940
