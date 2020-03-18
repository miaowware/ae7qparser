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
        url = base_url + "data/CallHistory.php?CALL=" + query
        super().__init__(tables, query, url)

        self.callsign_data = Table(tables[0][1:])

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

        for row in self.callsign_data:
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
    def __init__(self, tables: Sequence[Table], query: str):
        url = base_url + "data/LicenseeIdHistory.php?ID=" + query
        super().__init__(tables, query, url)

        self.licensee_id_history = None
        self.application_history = None
        self.pending_applications = None

        for table in tables:
            if self.licensee_id_history is None and isinstance(table, LicenseeIdHistoryTable):
                self.licensee_id_history = table
            elif self.application_history is None and isinstance(table, VanityApplicationsHistoryTable):
                self.application_history = table
            elif self.pending_applications is None and isinstance(table, PendingApplicationsPredictionsTable):
                self.pending_applications = table


class Ae7qFrnData(Ae7qData):
    # http://ae7q.com/query/data/FrnHistory.php?FRN=0016605636
    def __init__(self, tables: Sequence[Table], query: str):
        url = base_url + "data/FrnHistory.php?FRN=" + query
        super().__init__(tables, query, url)

        self.frn_history = None
        self.application_history = None
        self.pending_applications = None

        for table in tables:
            if self.frn_history is None and isinstance(table, FrnHistoryTable):
                self.frn_history = table
            elif self.application_history is None and isinstance(table, VanityApplicationsHistoryTable):
                self.application_history = table
            elif self.pending_applications is None and isinstance(table, PendingApplicationsPredictionsTable):
                self.pending_applications = table


class Ae7qApplicationData(Ae7qData):
    # http://ae7q.com/query/data/AppDetail.php?UFN=0008963527
    def __init__(self, tables: Sequence[Table], query: str):
        url = base_url + "data/AppDetail.php?UFN=" + query
        super().__init__(tables, query, url)

        # tables
        self.application_data = Table(tables[0][2:])
        self.application_history = ApplicationActionHistoryTable(tables[1][1:]) if len(tables) > 1 else None
        self.vanity_callsigns = ApplicationVanityCallsignsTable(tables[2][1:]) if len(tables) > 2 else None

        # data
        self.frn = None
        self.licensee_id = None
        self.applicant_type = None
        self.entity_type = None
        self.entity_name = None
        self.attention = None
        self.first_name = None
        self.middle_initial = None
        self.last_name = None
        self.name_suffix = None
        self.street_address = None
        self.po_box = None
        self.locality = None
        self.county = None
        self.state = None
        self.postal_code = None
        self.zip_location = None
        self.maidenhead = None
        self.uls_geo_region = None
        self.callsign = None
        self.radio_service = None
        self.last_action_date = None
        self.receipt_date = None
        self.entered_timestamp = None
        self.application_source = None
        self.original_purpose = None
        self.application_purpose = None
        self.result = None
        self.fee_control_number = None
        self.payment_date = None
        self.original_receipt = None
        self.operator_class = None
        self.operator_group = None
        self.uls_group = None
        self.new_sequential_callsign = None
        self.vanity_type = None
        self.vanity_relationship = None
        self.is_from_vec = None
        self.is_trustee = None
        self.trustee_callsign = None
        self.trustee_name = None

        for row in self.application_data:
            if self.frn is None and row[0] == "FRN":
                self.frn = row[1]
            elif self.licensee_id is None and row[0] == "Licensee ID/SGIN":
                self.licensee_id = row[1]
            elif self.applicant_type is None and row[0] == "Applicant Type":
                self.applicant_type = row[1]
            elif self.entity_type is None and row[0] == "Entity Type":
                self.entity_type = row[1]
            elif self.entity_name is None and row[0] == "Entity Name":
                self.entity_name = row[1]
            elif self.attention is None and row[0] == "Attention":
                self.attention = row[1]
            elif self.first_name is None and row[0] == "First Name":
                self.first_name = row[1]
            elif self.middle_initial is None and row[0] == "Middle Init":
                self.middle_initial = row[1]
            elif self.last_name is None and row[0] == "Last Name":
                self.last_name = row[1]
            elif self.name_suffix is None and row[0] == "Name Suffix":
                self.name_suffix = row[1]
            elif self.street_address is None and row[0] == "Street Address":
                self.street_address = row[1]
            elif self.po_box is None and row[0] == "Po Box":
                self.po_box = row[1]
            elif self.locality is None and row[0] == "Locality":
                self.locality = row[1]
            elif self.county is None and row[0] == "County":
                self.county = row[1]
            elif self.state is None and row[0] == "State":
                self.state = row[1]
            elif self.postal_code is None and row[0] == "Postal Code":
                self.postal_code = row[1]
            elif (self.zip_location is None or len(self.zip_location) == 1) and row[0] == "Zip Location":
                if self.zip_location is None:
                    self.zip_location = [row[1],]
                else:
                    self.zip_location.append(row[1])
                    self.zip_location = tuple(self.zip_location)
            elif self.maidenhead is None and row[0] == "Maidenhead":
                self.maidenhead = row[1]
            elif self.uls_geo_region is None and row[0] == "ULS/Geo Region":
                self.uls_geo_region = row[1]
            elif self.callsign is None and row[0] == "Callsign":
                self.callsign = row[1]
            elif self.radio_service is None and row[0] == "Radio Service":
                self.radio_service = row[1]
            elif self.last_action_date is None and row[0] == "Last Action Date":
                self.last_action_date = row[1]
            elif self.receipt_date is None and row[0] == "Receipt Date":
                self.receipt_date = row[1]
            elif self.entered_timestamp is None and row[0] == "Entered Timestamp":
                self.entered_timestamp = row[1]
            elif self.application_source is None and row[0] == "App Source":
                self.application_source = row[1]
            elif self.original_purpose is None and row[0] == "Orig Purpose":
                self.original_purpose = row[1]
            elif self.application_purpose is None and row[0] == "App Purpose":
                self.application_purpose = row[1]
            elif self.result is None and row[0] == "Result":
                self.result = row[1]
            elif self.fee_control_number is None and row[0] == "Fee Control Num":
                self.fee_control_number = row[1]
            elif self.payment_date is None and row[0] == "Payment Date":
                self.payment_date = row[1]
            elif self.original_receipt is None and row[0] == "Orig Receipt":
                self.original_receipt = row[1]
            elif self.operator_class is None and row[0] == "Operator Class":
                self.operator_class = row[1]
            elif self.operator_group is None and row[0] == "Operator Group":
                self.operator_group = row[1]
            elif self.uls_group is None and row[0] == "Uls Group":
                self.uls_group = row[1]
            elif self.new_sequential_callsign is None and row[0] == "New Seq Callsign":
                self.new_sequential_callsign = True if row[1] == "Y" else False
            elif self.vanity_type is None and row[0] == "Vanity Type":
                self.vanity_type = row[1]
            elif self.vanity_relationship is None and row[0] == "Vanity Relationship":
                self.vanity_relationship = row[1]
            elif self.is_from_vec is None and row[0] == "Is From Vec":
                self.is_from_vec = True if row[1] == "Y" else False
            elif self.is_trustee is None and row[0] == "Is Trustee":
                self.is_trustee = True if row[1] == "Y" else False
            elif self.trustee_callsign is None and row[0] == "Trustee Callsign":
                self.trustee_callsign = row[1]
            elif self.trustee_name is None and row[0] == "Trustee Name":
                self.trustee_name = row[1]

# other queries:
# maybe for future?
# http://ae7q.com/query/list/AppByReceipt.php?DATE=2018-06-08
# http://www.ae7q.com/query/list/ProcessDate.php?DATE=yesterday
# http://www.ae7q.com/query/list/CallByZip.php?ZIP5=07940
