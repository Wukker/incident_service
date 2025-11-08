from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.infra.sqla.utils import init_db


@asynccontextmanager
async def lifespan_setup(
    app: FastAPI,
) -> AsyncGenerator[None, None]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    app.middleware_stack = None
    app.middleware_stack = app.build_middleware_stack()

    init_db(app)

    yield

    await app.state.db_engine.dispose()
