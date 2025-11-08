import logging
from dataclasses import dataclass
from uuid import UUID

from src.application.common.body_params.incident import IncidentUpdateParams
from src.application.common.ports.incident_reader import IncidentReader
from src.application.common.ports.incident_writer import IncidentWriter
from src.domain.enums.incident_status import IncidentStatus
from src.domain.exceptions.incident import (
    IncidentAlreadyHasStatusError,
    IncidentNotFoundError,
)

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateIncidentRequest:
    incident_id: UUID
    status: IncidentStatus


class UpdateIncidentInteractor:
    def __init__(
        self,
        incident_writer_gateway: IncidentWriter,
        incident_reader_gateway: IncidentReader,
    ):
        self._incident_writer_gateway = incident_writer_gateway
        self._incident_reader_gateway = incident_reader_gateway

    async def execute(
        self,
        request_data: UpdateIncidentRequest,
    ) -> None:
        log.info(
            "Update incident: started." f"Id is {request_data.incident_id}",
        )

        incident = await self._incident_reader_gateway.get(
            request_data.incident_id,
        )
        if incident is None:
            raise IncidentNotFoundError(request_data.incident_id)

        if incident["status"] == request_data.status:
            raise IncidentAlreadyHasStatusError(request_data.incident_id)

        incident_update_params = IncidentUpdateParams(
            incident_status=request_data.status,
        )
        log.info(
            incident,
        )
        await self._incident_writer_gateway.update(
            incident["id_"],
            incident_update_params,
        )

        log.info(
            "Update incident: done. Incident new status is: '%s'.",
            request_data.status,
        )
        return None
