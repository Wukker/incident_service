from enum import StrEnum


class IncidentSource(StrEnum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"
