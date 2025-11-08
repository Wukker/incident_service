from datetime import UTC, datetime

from src.domain.entities.incident import Incident
from src.domain.enums.incident_source import IncidentSource
from src.domain.enums.incident_status import IncidentStatus
from src.domain.ports.uuid_generator import UuidIdGenerator


class IncidentService:
    def __init__(
        self,
    ) -> None:
        self._user_id_generator = UuidIdGenerator()

    def create_incident(
        self,
        description: str,
        source: IncidentSource = IncidentSource.MONITORING,
    ) -> Incident:
        """
        :raises RoleAssignmentNotPermittedError:
        :raises DomainFieldError:
        """
        incident_id = self._user_id_generator()
        return Incident(
            id_=incident_id,
            description=description,
            status=IncidentStatus.OPEN,
            source=source,
            created_at=datetime.now(UTC),
        )
