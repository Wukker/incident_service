from typing import (
    Annotated,
    Optional,
)
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.body_params.incident import IncidentUpdateParams
from src.application.common.ports.incident_reader import IncidentReader
from src.application.common.ports.incident_writer import IncidentWriter
from src.application.common.query_models.incident import IncidentQueryModel
from src.application.common.query_params.incident import IncidentReadParams
from src.domain.entities.incident import Incident
from src.infra.sqla.models.incident import IncidentModel

from src.infra.sqla.dependencies import get_db_session


class IncidentSqlaAdapter(IncidentReader, IncidentWriter):
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_db_session)],
    ) -> None:
        self.session = session

    async def add(
        self,
        incident: Incident,
    ) -> None:
        model = IncidentModel(
            id=incident.id_,
            description=incident.description,
            status=incident.status,
            source=incident.source,
            created_at=incident.created_at,
        )

        self.session.add(model)
        await self.session.flush([model])

    async def get(self, incident_id: UUID) -> Optional[IncidentQueryModel]:
        query = select(IncidentModel).where(IncidentModel.id == incident_id)

        response = await self.session.execute(query)
        model = response.scalar()
        if model is None:
            return None
        incident = IncidentQueryModel(
            id_=model.id,
            description=model.description,
            status=model.status,
            source=model.source,
            created_at=model.created_at,
        )
        return incident

    async def list(
        self,
        incident_read_params: IncidentReadParams,
    ) -> list[IncidentQueryModel]:
        query = select(IncidentModel)
        status = incident_read_params.incident_status
        if status is not None:
            query = query.where(IncidentModel.status == status)

        response = await self.session.execute(query)
        models = response.scalars().all()
        return [
            IncidentQueryModel(
                id_=model.id,
                description=model.description,
                status=model.status,
                source=model.source,
                created_at=model.created_at,
            )
            for model in models
        ]

    async def update(
        self,
        incident_id: UUID,
        incident_update_params: IncidentUpdateParams,
    ) -> None:
        query = (
            update(IncidentModel)
            .where(IncidentModel.id == incident_id)
            .values(status=incident_update_params.incident_status)
        )

        await self.session.execute(query)
