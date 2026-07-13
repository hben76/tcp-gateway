# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Health check",
    description="Returns the application health status.",
)
async def health():
    return {"status": "UP"}
