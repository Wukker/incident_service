from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    DateTime,
    String,
    Uuid,
    func,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.enums.incident_status import IncidentStatus
from src.domain.enums.incident_source import IncidentSource
from src.infra.sqla.models.base import Base


class IncidentModel(Base):
    """Модель инцидентов."""

    __tablename__ = "incidents"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
    )
    """Идентификатор инцидента."""

    description: Mapped[str] = mapped_column(String(), nullable=False)
    """Описание инцидента."""

    status: Mapped[IncidentStatus] = mapped_column(
        ENUM(IncidentStatus),
        nullable=False,
        index=True,
    )
    """Статус инцидента."""

    source: Mapped[IncidentSource] = mapped_column(
        ENUM(IncidentSource),
        nullable=False,
    )
    """Источник инцидента."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    """Дата создания инцидента."""
