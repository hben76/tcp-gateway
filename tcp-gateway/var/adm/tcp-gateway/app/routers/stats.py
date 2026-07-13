# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# stats.py
#

"""
Runtime statistics router.
"""

from fastapi import APIRouter

from app.models.statistics import StatisticsResponse
from app.services.statistics_service import statistics_service

router = APIRouter(
    tags=["Statistics"],
)


@router.get(
    "/stats",
    response_model=StatisticsResponse,
    summary="Runtime statistics",
    description="Returns runtime statistics for the TCP Gateway service.",
)
async def get_statistics() -> StatisticsResponse:
    """
    Return runtime statistics.
    """

    return statistics_service.snapshot()
