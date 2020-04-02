"""
tables.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


from typing import Sequence

from .base import Row, Table


class ConditionsRow(Row):
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.conditions = row_data[0]


class ConditionsTable(Table):
    row_cls = ConditionsRow  # Class attribute


class CallHistoryRow(Row):
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.entity_name = row_data[0]
        self.applicant_type = row_data[1]
        self.operator_class = row_data[2]
        self.region_state = row_data[3]
        self.license_status = row_data[4]
        self.grant_date = row_data[5]
        self.effective_date = row_data[6]
        self.cancel_date = row_data[7]
        self.expire_date = row_data[8]


class CallHistoryTable(Table):
    row_cls = CallHistoryRow


class TrusteeRow(Row):
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.callsign = row_data[0]
        self.region_state = row_data[1]
        self.entity_name = row_data[2]
        self.applicant_type = row_data[3]
        self.license_status = row_data[4]
        self.grant_date = row_data[5]
        self.effective_date = row_data[6]
        self.cancel_date = row_data[7]
        self.expire_date = row_data[8]


class TrusteeTable(Table):
    row_cls = TrusteeRow


class ApplicationsHistoryRow(Row):
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.receipt_date = row_data[0]
        self.application_callsign = row_data[1]
        self.region_state = row_data[2]
        self.entity_name = row_data[3]
        self.uls_file_number = row_data[4].strip("(Batch)").strip("(Online)")
        self.application_purpose = row_data[5]
        self.payment_date = row_data[6]
        self.last_action_date = row_data[7]
        self.application_status = row_data[8]


class ApplicationsHistoryTable(Table):
    row_cls = ApplicationsHistoryRow


class VanityApplicationsHistoryRow(ApplicationsHistoryRow):
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.applied_callsigns = row_data[9]


class VanityApplicationsHistoryTable(Table):
    row_cls = VanityApplicationsHistoryRow


class PendingApplicationsPredictionsRow(Row):
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.receipt_date = row_data[0]
        self.process_date = row_data[1]
        self.applicant_callsign = row_data[2]
        self.region_state = row_data[3]
        self.operator_class = row_data[4]
        self.uls_file_number = row_data[5].strip("(Batch)").strip("(Online)")
        self.vanity_type = row_data[6]
        self.sequential_number = row_data[7]
        self.vanity_callsign = row_data[8]
        self.prediction = row_data[9]


class PendingApplicationsPredictionsTable(Table):
    row_cls = PendingApplicationsPredictionsRow


class EventCallsignRow(Row):
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.start_date = row_data[0]
        self.end_date = row_data[1]
        self.event_callsign = row_data[2]
        self.entity_name = row_data[3]
        self.event_name = row_data[4]


class EventCallsignTable(Table):
    row_cls = EventCallsignRow


class FrnHistoryRow(Row):
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.callsign = row_data[0]
        self.region_state = row_data[1]
        self.entity_name = row_data[2]
        self.applicant_type = row_data[3]
        self.operator_class = row_data[4]
        self.license_status = row_data[5]
        self.grant_date = row_data[6]
        self.effective_date = row_data[7]
        self.cancel_date = row_data[8]
        self.expire_date = row_data[9]


class FrnHistoryTable(Table):
    row_cls = FrnHistoryRow


class LicenseeIdHistoryRow(Row):
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.callsign = row_data[0]
        self.region_state = row_data[1]
        self.entity_name = row_data[2]
        self.applicant_type = row_data[3]
        self.operator_class = row_data[4]
        self.license_status = row_data[5]
        self.grant_date = row_data[6]
        self.effective_date = row_data[7]
        self.cancel_date = row_data[8]
        self.expire_date = row_data[9]


class LicenseeIdHistoryTable(Table):
    row_cls = LicenseeIdHistoryRow


class ApplicationActionHistoryRow(Row):
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.action_date = row_data[0]
        self.action_type = row_data[1]


class ApplicationActionHistoryTable(Table):
    row_cls = ApplicationActionHistoryRow


class ApplicationVanityCallsignsRow(Row):
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.sequence_number = row_data[0]
        self.callsign = row_data[1]
        self.prediction = row_data[2] if len(row_data) == 3 else None


class ApplicationVanityCallsignsTable(Table):
    row_cls = ApplicationVanityCallsignsRow


class ApplicationAttachmentsRow(Row):
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.date = row_data[0]
        self.type = row_data[1]
        self.description = row_data[2]
        self.result = row_data[3]


class ApplicationAttachmentsTable(Table):
    row_cls = ApplicationAttachmentsRow
