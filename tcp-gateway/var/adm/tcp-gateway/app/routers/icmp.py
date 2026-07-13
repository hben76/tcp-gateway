# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# icmp.py
#

"""
ICMP connectivity router.
"""

from fastapi import APIRouter, Depends
from starlette.concurrency import run_in_threadpool

from app.models.icmp import (
    IcmpCheckRequest,
    IcmpCheckResponse,
)
from app.models.responses import ErrorResponse
from app.security.api_key import verify_api_key
from app.services.icmp_service import IcmpService
from app.services.statistics_service import statistics_service

router = APIRouter(
    prefix="/v1/icmp",
    tags=["ICMP"],
)

service = IcmpService()


@router.post(
    "/check",
    response_model=IcmpCheckResponse,
    responses={
        401: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Check ICMP connectivity",
    description="Perform a single ICMP ping connectivity check.",
)
async def check_icmp(
    request: IcmpCheckRequest,
    _: None = Depends(verify_api_key),
) -> IcmpCheckResponse:
    """
    Check ICMP connectivity.
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
