# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson

from fastapi import APIRouter

from app.config import config

router = APIRouter(tags=["Version"])


@router.get(
    "/version",
    summary="Application version",
    description="Returns application information.",
)
async def version():

    return {
        "application": config.application.name,
        "version": config.application.version,
    }
