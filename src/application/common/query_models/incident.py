from datetime import datetime
from typing import TypedDict
from uuid import UUID

from src.domain.enums.incident_source import IncidentSource
from src.domain.enums.incident_status import IncidentStatus


class IncidentQueryModel(TypedDict):
    id_: UUID
    description: str
    status: IncidentStatus
    source: IncidentSource
    created_at: datetime
