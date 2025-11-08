import logging
from dataclasses import dataclass
from typing import TypedDict
from uuid import UUID

from src.application.common.ports.incident_writer import IncidentWriter
from src.domain.enums.incident_source import IncidentSource
from src.domain.services.incident import IncidentService

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateIncidentRequest:
    description: str
    source: IncidentSource


class CreateIncidentResponse(TypedDict):
    id: UUID


class CreateIncidentInteractor:
    def __init__(
        self,
        incident_writer_gateway: IncidentWriter,
    ):
        self._incident_service = IncidentService()
        self._incident_command_gateway = incident_writer_gateway

    async def execute(
        self,
        request_data: CreateIncidentRequest,
    ) -> CreateIncidentResponse:
        log.info(
            "Create incident: started.",
        )

        description = request_data.description
        source = request_data.source

        incident = self._incident_service.create_incident(description, source)
        await self._incident_command_gateway.add(incident)

        log.info("Create incident: done. Incident id: '%s'.", incident.id_)
        return CreateIncidentResponse(id=incident.id_)
