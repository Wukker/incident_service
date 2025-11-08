from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.application.common.query_models.incident import IncidentQueryModel
from src.application.common.query_params.incident import IncidentReadParams


class IncidentReader(Protocol):
    @abstractmethod
    async def get(
        self,
        incident_id: UUID,
    ) -> IncidentQueryModel | None:
        """:raises ReaderError:"""

    @abstractmethod
    async def list(
        self,
        incident_read_params: IncidentReadParams,
    ) -> list[IncidentQueryModel]:
        """:raises ReaderError:"""
