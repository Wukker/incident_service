import logging
from dataclasses import dataclass
from typing import TypedDict

from src.application.common.ports.incident_reader import IncidentReader
from src.application.common.query_models.incident import IncidentQueryModel
from src.application.common.query_params.incident import IncidentReadParams
from src.domain.enums.incident_status import IncidentStatus

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ListIncidentsRequest:
    incident_status: IncidentStatus | None = None


class ListIncidentsResponse(TypedDict):
    incidents: list[IncidentQueryModel]


class ListIncidentsQueryService:
    def __init__(
        self,
        incident_reader_gateway: IncidentReader,
    ):
        self._incident_reader_gateway = incident_reader_gateway

    async def execute(
        self,
        request_data: ListIncidentsRequest,
    ) -> ListIncidentsResponse:
        log.info("List incidents: started.")

        incident_read_params = IncidentReadParams(
            incident_status=request_data.incident_status,
        )

        incidents: list[IncidentQueryModel] = await self._incident_reader_gateway.list(
            incident_read_params,
        )

        response = ListIncidentsResponse(incidents=incidents)

        log.info("List incidents: done.")
        return response
