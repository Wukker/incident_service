from dataclasses import dataclass
from typing import Optional

from src.domain.enums.incident_status import IncidentStatus


@dataclass(frozen=True, slots=True)
class IncidentReadParams:
    incident_status: Optional[IncidentStatus] = None
