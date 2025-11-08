from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.application.common.body_params.incident import IncidentUpdateParams
from src.domain.entities.incident import Incident


class IncidentWriter(Protocol):
    @abstractmethod
    async def add(
        self,
        incident: Incident,
    ) -> None:
        """:raises ReaderError:"""

    @abstractmethod
    async def update(
        self,
        incident_id: UUID,
        incident_update_params: IncidentUpdateParams,
    ) -> None:
        """:raises ReaderError:"""
