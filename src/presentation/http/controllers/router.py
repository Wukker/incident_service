from fastapi.routing import APIRouter

from src.presentation.http.controllers import incident


api_router = APIRouter()
api_router.include_router(
    incident.router,
    prefix="/incidents",
    tags=["Incidents"],
)
