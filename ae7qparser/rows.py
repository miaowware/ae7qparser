"""
rows.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""

import collections.abc as abc
from typing import Sequence, Union


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
    """Base class representing an :class:`ae7qparser.tables.Table` row. The row's data can be accessed like a sequence.

    :param row_data: the data to store in the row.
    :type row_data: Sequence
    """
    def __init__(self, row_data: Sequence):
        self._data = tuple(row_data)

    @property
    def csv(self) -> str:
        """Convert the row's data to semicolon-separated format.

        :return: the row data, with cells separated by semicolons.
        :rtype: str
        """
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

    def __getitem__(self, index: Union[int, slice]):
        return self._data[index]

    def __iter__(self):
        return iter(self._data)


class ConditionsRow(Row):
    """Class representing an :class:`ae7qparser.tables.ConditionsTable` row.

    :var conditions:
    :vartype conditions: str
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.conditions = row_data[0]


class CallHistoryRow(Row):
    """Class representing an :class:`ae7qparser.tables.CallHistoryTable` row.

    :var entity_name:
    :vartype entity_name: str
    :var applicant_type:
    :var operator_class:
    :var region_state:
    :var license_status:
    :var grant_date:
    :var effective_date:
    :var cancel_date:
    :var expire_date:
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
    """Class representing an :class:`ae7qparser.tables.TrusteeTable` row.

    :var callsign:
    :var region_state:
    :var entity_name:
    :var applicant_type:
    :var license_status:
    :var grant_date:
    :var effective_date:
    :var cancel_date:
    :var expire_date:
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
    """Class representing an :class:`ae7qparser.tables.ApplicationsHistoryTable` row.

    :var receipt_date:
    :var application_callsign:
    :var region_state:
    :var entity_name:
    :var uls_file_number:
    :vartype uls_file_number: Tuple[str], None
    :var application_purpose:
    :var payment_date:
    :var last_action_date:
    :var application_status:
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
    """Class representing an :class:`ae7qparser.tables.VanityApplicationsHistoryTable` row.

    :var receipt_date:
    :var application_callsign:
    :var region_state:
    :var operator_class:
    :var uls_file_number:
    :vartype uls_file_number: Tuple[str]
    :var application_purpose:
    :var payment_date:
    :var last_action_date:
    :var application_status:
    :var applied_callsigns:
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
    """Class representing an :class:`ae7qparser.tables.PendingApplicationsPredictionsTable` row.

    :var receipt_date:
    :var process_date:
    :var applicant_callsign:
    :var region_state:
    :var operator_class:
    :var uls_file_number:
    :var vanity_type:
    :var sequential_number:
    :var vanity_callsign:
    :var prediction:
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
    """Class representing an :class:`ae7qparser.tables.CallsignPendingApplicationsPredictionsTable` row.

    :var receipt_date:
    :var process_date:
    :var applicant_callsign:
    :var operator_class:
    :var region_state:
    :var uls_file_number:
    :var vanity_type:
    :var sequential_number:
    :var prediction:
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
    """Class representing an :class:`ae7qparser.tables.EventCallsignTable` row.

    :var start_date:
    :var end_date:
    :var callsign:
    :var entity_name:
    :var event_name:
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.start_date = row_data[0]
        self.end_date = row_data[1]
        self.callsign = row_data[2]
        self.entity_name = row_data[3]
        self.event_name = row_data[4]


class FrnHistoryRow(Row):
    """Class representing an :class:`ae7qparser.tables.FrnHistoryTable` row.

    :var callsign:
    :var region_state:
    :var entity_name:
    :var applicant_type:
    :var operator_class:
    :var license_status:
    :var grant_date:
    :var effective_date:
    :var cancel_date:
    :var expire_date:
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
    """Class representing an :class:`ae7qparser.tables.LicenseeIdHistoryTable` row.

    :var callsign:
    :var region_state:
    :var entity_name:
    :var applicant_type:
    :var operator_class:
    :var license_status:
    :var grant_date:
    :var effective_date:
    :var cancel_date:
    :var expire_date:
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
    """Class representing an :class:`ae7qparser.tables.ApplicationActionHistoryTable` row.

    :var action_date:
    :var action_type:
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.action_date = row_data[0]
        self.action_type = row_data[1]


class ApplicationVanityCallsignsRow(Row):
    """Class representing an :class:`ae7qparser.tables.ApplicationVanityCallsignsTable` row.

    :var sequence_number:
    :var callsign:
    :var prediction:
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.sequence_number = row_data[0]
        self.callsign = row_data[1]
        self.prediction = row_data[2] if len(row_data) == 3 else None


class ApplicationAttachmentsRow(Row):
    """Class representing an :class:`ae7qparser.tables.ApplicationAttachmentsTable` row.

    :var date:
    :var type:
    :var description:
    :var result:
    """
    def __init__(self, row_data: Sequence):
        super().__init__(row_data)
        self.date = row_data[0]
        self.type = row_data[1]
        self.description = row_data[2]
        self.result = row_data[3]
