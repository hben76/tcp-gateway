# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# http.py
#

"""
HTTP connectivity router.
"""

from fastapi import APIRouter, Depends
from starlette.concurrency import run_in_threadpool

from app.models.http import (
    HttpCheckRequest,
    HttpCheckResponse,
    HttpWaitRequest,
    HttpWaitResponse,
)
from app.models.responses import ErrorResponse
from app.security.api_key import verify_api_key
from app.services.http_service import HttpService
from app.services.statistics_service import statistics_service

router = APIRouter(
    prefix="/v1/http",
    tags=["HTTP"],
)

service = HttpService()


@router.post(
    "/check",
    response_model=HttpCheckResponse,
    responses={
        401: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Check HTTP connectivity",
    description="Perform a single HTTP or HTTPS connectivity check.",
)
async def check_http(
    request: HttpCheckRequest,
    _: None = Depends(verify_api_key),
) -> HttpCheckResponse:
    """
    Check HTTP connectivity.
    """

    statistics_service.request_started()

    try:
        response = await run_in_threadpool(
            service.check,
            request,
        )

        statistics_service.record_check(response.reachable)

        return response

    finally:
        statistics_service.request_finished()


@router.post(
    "/wait",
    response_model=HttpWaitResponse,
    responses={
        401: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Wait for HTTP connectivity",
    description="Wait until an HTTP or HTTPS endpoint becomes available.",
)
async def wait_http(
    request: HttpWaitRequest,
    _: None = Depends(verify_api_key),
) -> HttpWaitResponse:
    """
    Wait for HTTP connectivity.
    """

    statistics_service.request_started()

    try:
        response = await run_in_threadpool(
            service.wait,
            request,
        )

        statistics_service.record_check(response.reachable)

        return response

    finally:
        statistics_service.request_finished()
