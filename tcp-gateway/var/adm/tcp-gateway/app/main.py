# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# main.py
#

"""
TCP Gateway application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import config
from app.logger import configure_logging
from app.metadata import (
    CONTACT,
    DESCRIPTION,
    LICENSE_INFO,
    TAGS_METADATA,
    TITLE,
)
from app.middleware.exception_handler import register_exception_handlers
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.request_logger import RequestLoggingMiddleware
from app.routers.api import router as api_router
from app.routers.health import router as health_router
from app.routers.http import router as http_router
from app.routers.icmp import router as icmp_router
from app.routers.ssh import router as ssh_router
from app.routers.stats import router as stats_router
from app.routers.tcp import router as tcp_router
from app.routers.version import router as version_router
from app.version import __version__


logger = configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown.
    """

    logger.info("Starting %s %s", TITLE, __version__)
    logger.info(
        "Listening on %s:%s",
        config.server.host,
        config.server.port,
    )
    logger.info(
        "Swagger UI: http://%s:%s/api/docs",
        config.server.host,
        config.server.port,
    )
    logger.info(
        "OpenAPI: http://%s:%s/api/openapi.json",
        config.server.host,
        config.server.port,
    )

    yield

    logger.info("Stopping %s", TITLE)


#
# FastAPI application
#

app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    version=__version__,
    contact=CONTACT,
    license_info=LICENSE_INFO,
    openapi_tags=TAGS_METADATA,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

#
# Middleware
#

app.add_middleware(RequestIDMiddleware)
app.add_middleware(RequestLoggingMiddleware)

#
# Exception Handlers
#

register_exception_handlers(app)

#
# Routers
#

app.include_router(health_router)
app.include_router(version_router)
app.include_router(stats_router)
app.include_router(api_router)

#
# Protocol Routers
#

app.include_router(tcp_router)
app.include_router(ssh_router)
app.include_router(http_router)
app.include_router(icmp_router)
