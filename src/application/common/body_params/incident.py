from dataclasses import dataclass

from src.domain.enums.incident_status import IncidentStatus


@dataclass(frozen=True, slots=True)
class IncidentUpdateParams:
    incident_status: IncidentStatus
