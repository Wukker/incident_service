"""Pydantic schemas for Swagger UI."""

from pydantic import BaseModel, ConfigDict, Field

from src.domain.enums.incident_source import IncidentSource
from src.domain.enums.incident_status import IncidentStatus


class CreateIncidentRequestPydantic(BaseModel):
    model_config = ConfigDict(frozen=True)

    description: str
    source: IncidentSource = Field(default=IncidentSource.MONITORING)


class UpdateIncidentRequestPydantic(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: IncidentStatus = Field()


class ListIncidentsRequestPydantic(BaseModel):
    status: IncidentStatus | None = Field(
        default=None,
    )
