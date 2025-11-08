import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import UJSONResponse
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.presentation.http.controllers.router import api_router
from src.setup.config.lifespan import lifespan_setup
from src.setup.config.logs import configure_logging
from src.setup.config.settings import settings


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="ucar",
        version="0.1.0",
        docs_url="/api/docs" if settings.enable_doc else None,
        redoc_url="/api/redoc" if settings.enable_doc else None,
        openapi_url="/api/openapi.json" if settings.enable_doc else None,
        default_response_class=UJSONResponse,
        lifespan=lifespan_setup,
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    @app.exception_handler(RequestValidationError)
    async def log_validation_errors(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        body = await request.body()
        logging.error(f"Validation error for body: {body.decode()}")
        logging.error(f"Errors: {exc.errors()}")
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    return app
