from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi_error_map import ErrorAwareRouter
from starlette import status

from src.application.commands.create_incident import (
    CreateIncidentInteractor,
    CreateIncidentRequest,
    CreateIncidentResponse,
)
from src.application.commands.update_incident import (
    UpdateIncidentInteractor,
    UpdateIncidentRequest,
)
from src.application.queries.list_incidents import (
    ListIncidentsQueryService,
    ListIncidentsRequest,
    ListIncidentsResponse,
)
from src.domain.exceptions.incident import (
    IncidentAlreadyHasStatusError,
    IncidentNotFoundError,
)
from src.infra.adapters.dependencies import (
    get_create_incident_sqla_interactor,
    get_list_incidents_sqla_service,
    get_update_incident_sqla_interactor,
)
from src.presentation.http.controllers.incident.schemas import (
    CreateIncidentRequestPydantic,
    ListIncidentsRequestPydantic,
    UpdateIncidentRequestPydantic,
)

router = ErrorAwareRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=ListIncidentsResponse,
)
async def get_incidents(
    request: Annotated[ListIncidentsRequestPydantic, Depends()],
    interactor: Annotated[
        ListIncidentsQueryService,
        Depends(get_list_incidents_sqla_service),
    ],
) -> ListIncidentsResponse:
    request_data = ListIncidentsRequest(
        incident_status=request.status,
    )
    return await interactor.execute(request_data)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateIncidentResponse,
)
async def create_incident(
    request: CreateIncidentRequestPydantic,
    interactor: Annotated[
        CreateIncidentInteractor,
        Depends(get_create_incident_sqla_interactor),
    ],
) -> CreateIncidentResponse:
    """
    Создание инцидента.

    - **description**: описание инцидента.
    - **source**: источник инцидента (operator, monitoring, partner).
    """
    request_data = CreateIncidentRequest(
        description=request.description,
        source=request.source,
    )
    return await interactor.execute(request_data)


@router.patch(
    path="/{id_}",
    error_map={
        IncidentNotFoundError: status.HTTP_404_NOT_FOUND,
        IncidentAlreadyHasStatusError: status.HTTP_400_BAD_REQUEST,
    },
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Статус инцидента успешно обновлен.",
        },
    },
)
async def update_incident(
    incident_id: UUID,
    request: UpdateIncidentRequestPydantic,
    interactor: Annotated[
        UpdateIncidentInteractor,
        Depends(get_update_incident_sqla_interactor),
    ],
) -> None:
    """
    Обновление инцидента.

    - **id**: идентификатор инцидента.
    - **status**: статус инцидента (open, in_progress, closed).
    """
    request_data = UpdateIncidentRequest(
        incident_id=incident_id,
        status=request.status,
    )
    return await interactor.execute(request_data)
