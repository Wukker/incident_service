from uuid import UUID

from src.domain.exceptions.base import DomainError, DomainFieldError


class IncidentNotFoundError(DomainError):
    def __init__(self, incident_id: UUID):
        message = f"Incident with id {incident_id} is not found."
        super().__init__(message)


class IncidentAlreadyHasStatusError(DomainFieldError):
    def __init__(self, incident_id: UUID):
        message = f"Incident with id {incident_id} already has this status."
        super().__init__(message)
