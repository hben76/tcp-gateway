# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# exception_handler.py
#

"""
Global exception handlers.

Registers application-wide exception handlers to ensure all API
errors have a consistent response format.
"""

import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.constants import REQUEST_ID_HEADER
from app.models.responses import ErrorResponse

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers.

    Args:
        app:
            FastAPI application instance.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        """
        Handle FastAPI HTTP exceptions.
        """

        logger.warning(
            "HTTP %d: %s",
            exc.status_code,
            exc.detail,
        )

        response = ErrorResponse(
            code=exc.status_code,
            message=str(exc.detail),
            request_id=request.headers.get(REQUEST_ID_HEADER),
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump(exclude_none=True),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """
        Handle request validation errors.
        """

        logger.warning(
            "Validation failed: %s",
            exc.errors(),
        )

        response = ErrorResponse(
            code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            message="Validation failed",
            request_id=request.headers.get(REQUEST_ID_HEADER),
            errors=exc.errors(),
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content=response.model_dump(exclude_none=True),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Handle unexpected exceptions.
        """

        logger.exception(
            "Unhandled exception",
            exc_info=exc,
        )

        response = ErrorResponse(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            request_id=request.headers.get(REQUEST_ID_HEADER),
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.model_dump(exclude_none=True),
        )
