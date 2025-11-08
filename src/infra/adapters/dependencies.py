from typing import Annotated
from fastapi import Depends

from src.application.commands.create_incident import CreateIncidentInteractor
from src.application.commands.update_incident import UpdateIncidentInteractor
from src.application.queries.list_incidents import ListIncidentsQueryService
from src.infra.adapters.incident_adapter_sqla import IncidentSqlaAdapter


async def get_create_incident_sqla_interactor(
    adapter: Annotated[IncidentSqlaAdapter, Depends()],
) -> CreateIncidentInteractor:
    return CreateIncidentInteractor(
        adapter,
    )


async def get_update_incident_sqla_interactor(
    adapter: Annotated[IncidentSqlaAdapter, Depends()],
) -> UpdateIncidentInteractor:
    return UpdateIncidentInteractor(
        adapter,
        adapter,
    )


async def get_list_incidents_sqla_service(
    adapter: Annotated[IncidentSqlaAdapter, Depends()],
) -> ListIncidentsQueryService:
    return ListIncidentsQueryService(
        adapter,
    )
