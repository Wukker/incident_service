from datetime import datetime
from uuid import UUID

from src.domain.enums.incident_source import IncidentSource
from src.domain.enums.incident_status import IncidentStatus


class Incident:
    def __init__(
        self,
        *,
        id_: UUID,
        description: str,
        status: IncidentStatus,
        source: IncidentSource,
        created_at: datetime,
    ) -> None:
        self.id_ = id_
        self.description = description
        self.status = status
        self.source = source
        self.created_at = created_at
