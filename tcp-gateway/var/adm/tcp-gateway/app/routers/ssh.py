# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# ssh.py
#

"""
SSH connectivity router.
"""

from fastapi import APIRouter, Depends
from starlette.concurrency import run_in_threadpool

from app.models.responses import ErrorResponse
from app.models.ssh import (
    SshCheckRequest,
    SshCheckResponse,
)
from app.security.api_key import verify_api_key
from app.services.ssh_service import SshService
from app.services.statistics_service import statistics_service

router = APIRouter(
    prefix="/v1/ssh",
    tags=["SSH"],
)

service = SshService()


@router.post(
    "/check",
    response_model=SshCheckResponse,
    responses={
        401: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Check SSH connectivity",
    description="Verify that an SSH service is responding.",
)
async def check_ssh(
    request: SshCheckRequest,
    _: None = Depends(verify_api_key),
) -> SshCheckResponse:
    """
    Check SSH connectivity.
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
