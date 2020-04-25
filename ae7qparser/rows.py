"""
rows.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""

import collections.abc as abc
from typing import Sequence


__all__ = [
    "Row",
    "ConditionsRow",
    "CallHistoryRow",
    "TrusteeRow",
    "ApplicationsHistoryRow",
    "VanityApplicationsHistoryRow",
    "PendingApplicationsPredictionsRow",
    "CallsignPendingApplicationsPredictionsRow",
    "EventCallsignRow",
    "FrnHistoryRow",
    "LicenseeIdHistoryRow",
    "ApplicationActionHistoryRow",
    "ApplicationVanityCallsignsRow",
    "ApplicationAttachmentsRow",
]


class Row(abc.Sequence):
    """Row
    ------

    Class representing a table Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
    def __init__(self, row_data: Sequence):
        self._data = tuple(row_data)

    @property
    def csv(self) -> str:
        csv_data = []
        for cell in self._data:
            if isinstance(cell, list) or isinstance(cell, tuple):
                cell = ",".join(cell)
            csv_data.append(cell)
        return ";".join([str(cell) for cell in csv_data])

    def __str__(self):
        return str(self._data)

    # --- Wrappers to implement sequence-like functionality ---
    def __len__(self):
        return len(self._data)

    def __getitem__(self, index: int):
        return self._data[index]

    def __iter__(self):
        return iter(self._data)


class ConditionsRow(Row):
    """ConditionsRow
    ------

    Class representing a ConditionsTable Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Attributes:
        conditions (str)

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.conditions = row_data[0]


class CallHistoryRow(Row):
    """CallHistoryRow
    ------

    Class representing a CallHistoryTable Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Attributes:
        entity_name
        applicant_type
        operator_class
        region_state
        license_status
        grant_date
        effective_date
        cancel_date
        expire_date

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
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


class TrusteeRow(Row):
    """TrusteeRow
    ------

    Class representing a TrusteeTable Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Attributes:
        callsign
        region_state
        entity_name
        applicant_type
        license_status
        grant_date
        effective_date
        cancel_date
        expire_date

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
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


class ApplicationsHistoryRow(Row):
    """ApplicationsHistoryRow
    ------

    Class representing a ApplicationsHistoryTable Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Attributes:
        receipt_date
        application_callsign
        region_state
        entity_name
        uls_file_number: a tuple of the file number and the filing type as strings
        application_purpose
        payment_date
        last_action_date
        application_status

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.receipt_date = row_data[0]
        self.application_callsign = row_data[1]
        self.region_state = row_data[2]
        self.entity_name = row_data[3]
        ufn = row_data[4].split(" ")
        self.uls_file_number = (ufn[0], ufn[1].strip("()"))
        self.application_purpose = row_data[5]
        self.payment_date = row_data[6]
        self.last_action_date = row_data[7]
        self.application_status = row_data[8]


class VanityApplicationsHistoryRow(Row):
    """VanityApplicationsHistoryRow
    ------

    Class representing a VanityApplicationsHistoryTable Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Attributes:
        receipt_date
        application_callsign
        region_state
        operator_class
        uls_file_number: a tuple of the file number and the filing type as strings
        application_purpose
        payment_date
        last_action_date
        application_status
        applied_callsigns

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.receipt_date = row_data[0]
        self.application_callsign = row_data[1]
        self.region_state = row_data[2]
        self.operator_class = row_data[3]
        ufn = row_data[4].split(" ")
        self.uls_file_number = (ufn[0], ufn[1].strip("()"))
        self.application_purpose = row_data[5]
        self.payment_date = row_data[6]
        self.last_action_date = row_data[7]
        self.application_status = row_data[8]
        self.applied_callsigns = row_data[9]


class PendingApplicationsPredictionsRow(Row):
    """PendingApplicationsPredictionsRow
    ------

    Class representing a PendingApplicationsPredictionsTable Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Attributes:
        receipt_date
        process_date
        applicant_callsign
        region_state
        operator_class
        uls_file_number
        vanity_type
        sequential_number
        vanity_callsign
        prediction

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.receipt_date = row_data[0]
        self.process_date = row_data[1]
        self.applicant_callsign = row_data[2]
        self.region_state = row_data[3]
        self.operator_class = row_data[4]
        self.uls_file_number = row_data[5]
        self.vanity_type = row_data[6]
        self.sequential_number = row_data[7]
        self.vanity_callsign = row_data[8]
        self.prediction = row_data[9]


class CallsignPendingApplicationsPredictionsRow(Row):
    """CallsignPendingApplicationsPredictionsRow
    ------

    Class representing a CallsignPendingApplicationsPredictionsTable Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Attributes:
        receipt_date
        process_date
        applicant_callsign
        operator_class
        region_state
        uls_file_number
        vanity_type
        sequential_number
        prediction

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.receipt_date = row_data[0]
        self.process_date = row_data[1]
        self.applicant_callsign = row_data[2]
        self.operator_class = row_data[3]
        self.region_state = row_data[4]
        self.uls_file_number = row_data[5]
        self.vanity_type = row_data[6]
        self.sequential_number = row_data[7]
        self.prediction = row_data[8]


class EventCallsignRow(Row):
    """EventCallsignRow
    ------

    Class representing a EventCallsignTable Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Attributes:
        start_date
        end_date
        callsign
        entity_name
        event_name

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.start_date = row_data[0]
        self.end_date = row_data[1]
        self.callsign = row_data[2]
        self.entity_name = row_data[3]
        self.event_name = row_data[4]


class FrnHistoryRow(Row):
    """FrnHistoryRow
    ------

    Class representing a FrnHistoryTable Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Attributes:
        callsign
        region_state
        entity_name
        applicant_type
        operator_class
        license_status
        grant_date
        effective_date
        cancel_date
        expire_date

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
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


class LicenseeIdHistoryRow(Row):
    """LicenseeIdHistoryRow
    ------

    Class representing a LicenseeIdHistoryTable Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Attributes:
        callsign
        region_state
        entity_name
        applicant_type
        operator_class
        license_status
        grant_date
        effective_date
        cancel_date
        expire_date

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
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


class ApplicationActionHistoryRow(Row):
    """ApplicationActionHistoryRow
    ------

    Class representing a ApplicationActionHistoryTable Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Attributes:
        action_date
        action_type

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.action_date = row_data[0]
        self.action_type = row_data[1]


class ApplicationVanityCallsignsRow(Row):
    """ApplicationVanityCallsignsRow
    ------

    Class representing a ApplicationVanityCallsignsTable Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Attributes:
        sequence_number
        callsign
        prediction

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.sequence_number = row_data[0]
        self.callsign = row_data[1]
        self.prediction = row_data[2] if len(row_data) == 3 else None


class ApplicationAttachmentsRow(Row):
    """ApplicationAttachmentsRow
    ------

    Class representing a ApplicationAttachmentsTable Row.
    Initialised with the row's data.

    The row's data can be accessed like a sequence.

    Args:
        row_data (Sequence): the data to store in the row.

    Attributes:
        date
        type
        description
        result

    Properties:
        csv (str): returns the row data, with cells separated by semicolons.
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.date = row_data[0]
        self.type = row_data[1]
        self.description = row_data[2]
        self.result = row_data[3]
