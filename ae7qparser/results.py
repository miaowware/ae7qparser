"""
results.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


from typing import Sequence
from datetime import datetime

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
from .utils import base_url


__all__ = [
    "Ae7qData",
    "Ae7qCallData",
    "Ae7qCanadianCallData",
    "Ae7qLicenseeData",
    "Ae7qFrnData",
    "Ae7qApplicationData",
]


class Ae7qData:
    """Base class representing a query result from AE7Q.

    :param tables: The tables to be stored in this object.
    :type tables: Sequence[Table]
    :param query: The query used to generate the data in this object.
    :type query: str
    :param query_url: The URL of the query.
    :type query_url: str

    :var tables: The tables stored in this object.
    :vartype tables: tuple[Table]
    :var query: The query used to generate the data in this object.
    :vartype query: str
    :var query_url: The URL of the query.
    :vartype query_url: str
    :var query_time: The time at which the query was executed.
    :vartype query_time: datetime
    """
    def __init__(self, tables: Sequence[Table], query: str, query_url: str):
        self.tables = tuple(tables)
        self.query = query
        self.query_url = query_url
        self.query_time = datetime.utcnow()

    def __repr__(self):
        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__
        return (f"<{module}.{qualname} object at {hex(id(self))}, "
                f"query={self.query}, query_time={self.query_time}>")


class Ae7qCallData(Ae7qData):
    """Data container for the result of an AE7Q callsign query.

    Example query: http://ae7q.com/query/data/CallHistory.php?CALL=KA1AAA

    :param tables: The tables to be stored in the Ae7qData object.
    :type tables: Sequence[Table]
    :param query: The query used to generate the data in this Ae7qData object.
    :type query: str

    :var tables: The tables stored in this object.
    :vartype tables: tuple[Table]
    :var query: The query used to generate the data in this object.
    :vartype query: str
    :var query_url: The URL of the query.
    :vartype query_url: str
    :var query_time: The time at which the query was executed.
    :vartype query_time: datetime
    :var conditions: table of conditions for the callsign.
    :vartype conditions: ConditionsTable, None
    :var call_history: table of the callsign holder history.
    :vartype call_history: CallHistoryTable, None
    :var trustee_history: table of any callsigns the callsign holder has been trustee of.
    :vartype trustee_history: TrusteeTable, None
    :var application_history: table of applications for the callsign.
    :vartype application_history: ApplicationsHistoryTable, None
    :var event_callsign_history: table of event callsign holder history.
    :vartype event_callsign_history: EventCallsignTable, None
    """
    def __init__(self, tables: Sequence[Table], query: str):
        url = base_url + "data/CallHistory.php?CALL=" + query
        super().__init__(tables, query, url)

        self.conditions = None
        self.call_history = None
        self.trustee_history = None
        self.application_history = None
        self.pending_applications = None
        self.event_callsign_history = None

        for table in tables:
            if self.conditions is None and isinstance(table, ConditionsTable):
                self.conditions = table
            elif self.call_history is None and isinstance(table, CallHistoryTable):
                self.call_history = table
            elif self.trustee_history is None and isinstance(table, TrusteeTable):
                self.trustee_history = table
            elif self.application_history is None and isinstance(table, ApplicationsHistoryTable):
                self.application_history = table
            elif self.pending_applications is None and isinstance(table, CallsignPendingApplicationsPredictionsTable):
                self.pending_applications = table
            elif self.event_callsign_history is None and isinstance(table, EventCallsignTable):
                self.event_callsign_history = table


class Ae7qCanadianCallData(Ae7qData):
    """Data container for the result of an AE7Q callsign query, if the callsign is Canadian.

    Example URL for the query: http://ae7q.com/query/data/CallHistory.php?CALL=VA1AAA

    :param tables: The tables to be stored in this object.
    :type tables: Sequence[Table]
    :param query: The query used to generate the data in this object.
    :type query: str

    :var tables: The tables stored in this object.
    :vartype tables: tuple[Table]
    :var query: The query used to generate the data in this object.
    :vartype query: str
    :var query_url: The URL of the query.
    :vartype query_url: str
    :var query_time: The time at which the query was executed.
    :vartype query_time: datetime
    :var callsign_data: Table of data about the query result.
    :vartype callsign_data: Table, None
    :var callsign: the callsign of the query result.
    :vartype callsign: str, None
    :var given_names: the given names of the callsign holder.
    :vartype given_names: str, None
    :var surname: the surname of the callsign holder.
    :vartype surname: str, None
    :var address: the address of the callsign holder.
    :vartype address: str, None
    :var locality: the locality of the callsign holder.
    :vartype locality: str, None
    :var province: the province of the callsign holder.
    :vartype province: str, None
    :var postal_code: the postal code of the callsign holder.
    :vartype postal_code: str, None
    :var country: the country of the callsign holder.
    :vartype country: str, None
    :var region: the region of the callsign holder.
    :vartype region: str, None
    :var grid_square: the grid square of the callsign holder.
    :vartype grid_square: str, None
    :var qualifications: the license qualifications of the callsign holder.
    :vartype qualifications: str, None
    """
    def __init__(self, tables: Sequence[Table], query: str):
        url = base_url + "data/CallHistory.php?CALL=" + query
        super().__init__(tables, query, url)

        self.callsign_data = tables[0] if len(tables) > 0 else None

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

        if self.callsign_data is not None:
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
    """Data container for the result of an AE7Q licensee ID query.

    Example URL for the query: http://ae7q.com/query/data/LicenseeIdHistory.php?ID=L00264867

    :param tables: The tables to be stored in this object.
    :type tables: Sequence[Table]
    :param query: The query used to generate the data in this object.
    :type query: str

    :var tables: The tables stored in this object.
    :vartype tables: tuple[Table]
    :var query: The query used to generate the data in this object.
    :vartype query: str
    :var query_url: The URL of the query.
    :vartype query_url: str
    :var query_time: The time at which the query was executed.
    :vartype query_time: datetime
    :var licensee_id_history: table of license history for the licensee ID.
    :vartype licensee_id_history: LicenseeIdHistoryTable, None
    :var application_history: table of applications for the licensee ID.
    :vartype application_data: VanityApplicationsHistoryTable, None
    :var pending_applications: table of pending applications for the licensee ID.
    :vartype pending_applications: PendingApplicationsPredictionsTable, None
    """
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
    """Data container for the result of an AE7Q FRN query.

    Example URL for the query: http://ae7q.com/query/data/FrnHistory.php?FRN=0004003141

    :param tables: The tables to be stored in this object.
    :type tables: Sequence[Table]
    :param query: The query used to generate the data in this object.
    :type query: str

    :var tables: The tables stored in this object.
    :vartype tables: tuple[Table]
    :var query: The query used to generate the data in this object.
    :vartype query: str
    :var query_url: The URL of the query.
    :vartype query_url: str
    :var query_time: The time at which the query was executed.
    :vartype query_time: datetime
    :var frn_history: table of license history for the FRN.
    :vartype frn_history: FrnHistoryTable, None
    :var application_history: table of applications for the FRN.
    :vartype application_history: VanityApplicationsHistoryTable, None
    :var pending_applications: table of pending applications for the FRN.
    :vartype pending_applications: PendingApplicationsPredictionsTable, None
    """
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
    """Data container for the result of an AE7Q application query.

    Example URL for the query: http://ae7q.com/query/data/AppDetail.php?UFN=0008569299

    :param tables: The tables to be stored in this object.
    :type tables: Sequence[Table]
    :param query: The query used to generate the data in this object.
    :type query: str

    :var tables: The tables stored in this object.
    :vartype tables: tuple[Table]
    :var query: The query used to generate the data in this object.
    :vartype query: str
    :var query_url: The URL of the query.
    :vartype query_url: str
    :var query_time: The time at which the query was executed.
    :vartype query_time: datetime
    :var application_data: the application's data.
    :vartype application_data: Table, None
    :var action_history: the application's action history.
    :vartype action_history: ApplicationActionHistoryTable, None
    :var vanity_callsigns: the application's applied callsigns.
    :vartype vanity_callsigns: ApplicationVanityCallsignsTable, None
    :var attachments: the application's attachments.
    :vartype attachments: ApplicationAttachmentsTable, None
    :var frn: the applicant's FRN.
    :vartype frn: str, None
    :var licensee_id: the applicant's FRN.
    :vartype licensee_id: str, None
    :var applicant_type: the applicant's type (e.g. club, individual).
    :vartype applicant_type: str, None
    :var entity_type: the applicant's entity type (e.g. Licensee).
    :vartype entity_type: str, None
    :var entity_name: the applicant's entity name. This is sometimes the same as the other name fields.
    :vartype entity_name: str, None
    :var attention: the applicant's ATTN line for their address. This is sometimes the trustee of the club.
    :vartype attention: str, None
    :var first_name: the applicant's the applicant's first name.
    :vartype first_name: str, None
    :var middle_initial: the applicant's middle initial.
    :vartype middle_initial: str, None
    :var last_name: the applicant's last name.
    :vartype last_name: str, None
    :var name_suffix: the applicant's name suffix.
    :vartype name_suffix: str, None
    :var street_address: the applicant's street address.
    :vartype street_address: str, None
    :var po_box: the applicant's PO box number, if it exists.
    :vartype po_box: str, None
    :var locality: the applicant's locality.
    :vartype locality: str, None
    :var county: the applicant's county.
    :vartype county: str, None
    :var state: the applicant's state.
    :vartype state: str, None
    :var postal_code: the applicant's postal code.
    :vartype postal_code: str, None
    :var zip_location: the applicant's latitude and longitude based on ZIP code.
    :vartype zip_location: Tuple[str], None
    :var maidenhead: the applicant's grid square.
    :vartype maidenhead: str, None
    :var uls_geo_region: the applicant's geographic region (i.e. the number in the callsign based on address).
    :vartype uls_geo_region: str, None
    :var callsign: the applicant's callsign.
    :vartype callsign: str, None
    :var radio_service: the applicant's radio service code.
    :vartype radio_service: str, None
    :var last_action_date: the application's last action date.
    :vartype last_action_date: datetime, None
    :var receipt_date: the application's receipt date.
    :vartype receipt_date: datetime, None
    :var entered_timestamp: the timestamp when the application was entered.
    :vartype entered_timestamp: datetime, None
    :var application_source: where the application was filed.
    :vartype application_source: str, None
    :var original_purpose: the application's original purpose.
    :vartype original_purpose: str, None
    :var application_purpose: the application's purpose.
    :vartype application_purpose: str, None
    :var result: the application's result.
    :vartype result: str, None
    :var fee_control_number: the application's fee control number. Probably blank, as no fees are collected now.
    :vartype fee_control_number: str, None
    :var payment_date: the application's payment date. Probably blank, as no fees are collected now.
    :vartype payment_date: datetime, None
    :var original_receipt: the application's original receipt date.
    :vartype original_receipt: datetime, None
    :var operator_class: the applicant's operator class.
    :vartype operator_class: str, None
    :var operator_group: the applicant's operator group.
    :vartype operator_group: str, None
    :var uls_group: the applicant's callsign group (A, B, C, or D)
    :vartype uls_group: str, None
    :var new_sequential_callsign: whether the applicant is applying for a new sequential callsign.
    :vartype new_sequential_callsign: str, None
    :var vanity_type: the type of vanity application.
    :vartype vanity_type: str, None
    :var vanity_relationship: the relationship of the previous callsign holder to the applicant.
    :vartype vanity_relationship: str, None
    :var is_from_vec: whether the application was filed by a VEC.
    :vartype is_from_vec: str, None
    :var is_trustee: whether the applicant is the trustee of the entity.
    :vartype is_trustee: str, None
    :var trustee_callsign: the applicant's trustee's callsign (if the entity is a club).
    :vartype trustee_callsign: str, None
    :var trustee_name: the applicant's trustee's name (if the entity is a club).
    :vartype trustee_name: str, None
    """
    def __init__(self, tables: Sequence[Table], query: str):
        url = base_url + "data/AppDetail.php?UFN=" + query
        super().__init__(tables, query, url)

        # tables
        self.application_data = None
        self.action_history = None
        self.vanity_callsigns = None
        self.attachments = None

        for table in tables:
            if self.application_data is None and isinstance(table, Table) and table.col_names and table.col_names[0] == "Field Name":
                self.application_data = table
            elif self.action_history is None and isinstance(table, ApplicationActionHistoryTable):
                self.action_history = table
            elif self.vanity_callsigns is None and isinstance(table, ApplicationVanityCallsignsTable):
                self.vanity_callsigns = table
            elif self.attachments is None and isinstance(table, ApplicationAttachmentsTable):
                self.attachments = table

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

        if self.application_data is not None:
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
                        self.zip_location = [row[1], ]
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
