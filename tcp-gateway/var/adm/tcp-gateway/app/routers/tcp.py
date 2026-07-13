# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# tcp.py
#

"""
TCP connectivity router.
"""

from fastapi import APIRouter, Depends
from starlette.concurrency import run_in_threadpool

from app.models.responses import ErrorResponse
from app.models.tcp import (
    TcpCheckRequest,
    TcpCheckResponse,
    TcpWaitRequest,
    TcpWaitResponse,
)
from app.security.api_key import verify_api_key
from app.services.statistics_service import statistics_service
from app.services.tcp_service import TcpService

router = APIRouter(
    prefix="/v1/tcp",
    tags=["TCP"],
)

service = TcpService()


@router.post(
    "/check",
    response_model=TcpCheckResponse,
    responses={
        401: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Check TCP connectivity",
    description="Perform a TCP connectivity check.",
)
async def check_tcp(
    request: TcpCheckRequest,
    _: None = Depends(verify_api_key),
) -> TcpCheckResponse:
    """
    Check TCP connectivity.
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
    response_model=TcpWaitResponse,
    responses={
        401: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Wait for TCP connectivity",
    description="Wait until a TCP endpoint becomes reachable.",
)
async def wait_tcp(
    request: TcpWaitRequest,
    _: None = Depends(verify_api_key),
) -> TcpWaitResponse:
    """
    Wait for TCP connectivity.
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
