"""
results.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


from typing import Sequence
from datetime import datetime

from .tables import *
from .utils import base_url


class Ae7qData:
    """Ae7qData
    ------

    Class representing Ae7qData.
    Initialised with a sequence of Tables, a query, and a query_url.

    Args:
        tables (Sequence[Table]): the tables to be stored in the Ae7qData object.
        query (str): the query used to generate the data in this Ae7qData object.
        query_url (str): the URL of the query.

    Attributes:
        tables (tuple[Table]): the tables stored in the Ae7qData object.
        query (str): the query used to generate the data in this Ae7qData object.
        query_url (str): the URL of the query.
        query_time (DateTime): the time at which the query was executed.
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
    """Ae7qCallData
    ------

    Data container for the result of an AE7Q callsign query.
    Descended from Ae7qData.

    Example URL for the query: http://ae7q.com/query/data/CallHistory.php?CALL={{ callsign }}

    Args:
        tables (Sequence[Table]): the tables to be stored in the Ae7qData object.
        query (str): the query used to generate the data in this Ae7qData object.

    Attributes:
        tables (tuple[Table]): the tables stored in the Ae7qData object.
        query (str): the query used to generate the data in this Ae7qData object.
        query_url (str): the URL of the query.
        query_time (DateTime): the time at which the query was executed.
        conditions (ConditionsTable): table of conditions for the callsign.
        call_history (CallHistoryTable): table of the callsign holder history.
        trustee_history (TrusteeTable): table of any callsigns the callsign holder has been trustee of.
        application_history (ApplicationsHistoryTable): table of applications for the callsign.
        event_callsign_history (EventCallsignTable): table of event callsign holder history.
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
    """Ae7qCanadianCallData
    ------

    Data container for the result of an AE7Q callsign query, if the callsign is Canadian.
    Descended from Ae7qData.

    Example URL for the query: http://ae7q.com/query/data/CallHistory.php?CALL={{ callsign }}

    Args:
        tables (Sequence[Table]): the tables to be stored in the Ae7qData object.
        query (str): the query used to generate the data in this Ae7qData object.

    Attributes:
        tables (tuple[Table]): the tables stored in the Ae7qData object.
        query (str): the query used to generate the data in this Ae7qData object.
        query_url (str): the URL of the query.
        query_time (DateTime): the time at which the query was executed.
        callsign_data (Table):
        callsign: the callsign of the query result.
        given_names: the given names of the callsign holder.
        surname: the surname of the callsign holder.
        address: the address of the callsign holder.
        locality: the locality of the callsign holder.
        province: the province of the callsign holder.
        postal_code: the postal code of the callsign holder.
        country: the country of the callsign holder.
        region: the region of the callsign holder.
        grid_square: the grid square of the callsign holder.
        qualifications: the license qualifications of the callsign holder.
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
    """Ae7qLicenseeData
    ------

    Data container for the result of an AE7Q licensee ID query.
    Descended from Ae7qData.

    Example URL for the query: http://ae7q.com/query/data/LicenseeIdHistory.php?ID={{ licensee ID }}

    Args:
        tables (Sequence[Table]): the tables to be stored in the Ae7qData object.
        query (str): the query used to generate the data in this Ae7qData object.

    Attributes:
        tables (tuple[Table]): the tables stored in the Ae7qData object.
        query (str): the query used to generate the data in this Ae7qData object.
        query_url (str): the URL of the query.
        query_time (DateTime): the time at which the query was executed.
        licensee_id_history (LicenseeIdHistoryTable): table of license history for the licensee ID.
        application_history (VanityApplicationsHistoryTable): table of applications for the licensee ID.
        pending_applications (PendingApplicationsPredictionsTable): table of pending applications for the licensee ID.
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
    """Ae7qFrnData
    ------

    Data container for the result of an AE7Q FRN query.
    Descended from Ae7qData.

    Example URL for the query: http://ae7q.com/query/data/FrnHistory.php?FRN={{ FRN }}

    Args:
        tables (Sequence[Table]): the tables to be stored in the Ae7qData object.
        query (str): the query used to generate the data in this Ae7qData object.

    Attributes:
        tables (tuple[Table]): the tables stored in the Ae7qData object.
        query (str): the query used to generate the data in this Ae7qData object.
        query_url (str): the URL of the query.
        query_time (DateTime): the time at which the query was executed.
        frn_history (FrnHistoryTable): table of license history for the FRN.
        application_history (VanityApplicationsHistoryTable): table of applications for the licensee ID.
        pending_applications (PendingApplicationsPredictionsTable): table of pending applications for the licensee ID.
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
    """Ae7qApplicationData
    ------

    Data container for the result of an AE7Q application query.
    Descended from Ae7qData.

    Example URL for the query: http://ae7q.com/query/data/AppDetail.php?UFN={{ UFN }}

    Args:
        tables (Sequence[Table]): the tables to be stored in the Ae7qData object.
        query (str): the query used to generate the data in this Ae7qData object.

    Attributes:
        tables (tuple[Table]): the tables stored in the Ae7qData object.
        query (str): the query used to generate the data in this Ae7qData object.
        query_url (str): the URL of the query.
        query_time (DateTime): the time at which the query was executed.
        application_data (Table): the application's data.
        action_history (ApplicationActionHistoryTable): the application's action history.
        vanity_callsigns (ApplicationVanityCallsignsTable): the application's applied callsigns.
        attachments (ApplicationAttachmentsTable): the application's attachments.
        frn: the applicant's FRN.
        licensee_id: the applicant's FRN.
        applicant_type: the applicant's type (e.g. club, individual).
        entity_type: the applicant's entity type (e.g. Licensee).
        entity_name: the applicant's entity name. This is sometimes the same as the other name fields.
        attention: the applicant's ATTN line for their address. This is sometimes the trustee of the club.
        first_name: the applicant's the applicant's first name.
        middle_initial: the applicant's middle initial.
        last_name: the applicant's last name.
        name_suffix: the applicant's name suffix.
        street_address: the applicant's street address.
        po_box: the applicant's PO box number, if it exists.
        locality: the applicant's locality.
        county: the applicant's county.
        state: the applicant's state.
        postal_code: the applicant's postal code.
        zip_location: the applicant's location (tuple of lattitude and longitude) based on ZIP code.
        maidenhead: the applicant's grid square.
        uls_geo_region: the applicant's geographic region (i.e. the number in the callsign based on address).
        callsign: the applicant's callsign.
        radio_service: the applicant's radio service code.
        last_action_date: the application's last action date.
        receipt_date: the application's receipt date.
        entered_timestamp: the timestamp when the application was entered.
        application_source: where the application was filed.
        original_purpose: the application's original purpose.
        application_purpose: the application's purpose.
        result: the application's result.
        fee_control_number: the application's fee control number. Probably blank, as no fees are collected now.
        payment_date: the application's payment date. Probably blank, as no fees are collected now.
        original_receipt: the application's original receipt date.
        operator_class: the applicant's operator class.
        operator_group: the applicant's operator group.
        uls_group: the applicant's callsign group (A, B, C, or D)
        new_sequential_callsign: whether the applicant is applying for a new sequential callsign.
        vanity_type: the type of vanity application.
        vanity_relationship: the relationship of the previous callsign holder to the applicant.
        is_from_vec: whether the application was filed by a VEC.
        is_trustee: whether the applicant is the trustee of the entity.
        trustee_callsign: the applicant's trustee's callsign (if the entity is a club).
        trustee_name: the applicant's trustee's name (if the entity is a club).
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
            if self.application_data is None and isinstance(table, Table) and table.col_names[0] == "Field Name":
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
