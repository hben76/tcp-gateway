# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# API discovery endpoints
#

from fastapi import APIRouter

from app.config import config
from app.version import __version__

router = APIRouter(
    prefix="/api",
    tags=["API"],
)


@router.get(
    "",
    summary="API Landing Page",
)
async def api_root():

    return {
        "name": config.application.name,
        "version": __version__,
        "description": "Enterprise Connectivity Gateway",
        "documentation": {
            "swagger": "/api/docs",
            "redoc": "/api/redoc",
            "openapi": "/api/openapi.json",
        },
        "discovery": {
            "info": "/api/info",
            "examples": "/api/examples",
        },
    }


@router.get(
    "/info",
    summary="Gateway Information",
)
async def api_info():

    return {
        "application": {
            "name": config.application.name,
            "version": __version__,
        },
        "authentication": {
            "type": "API Key",
            "header": "X-API-Key",
        },
        "protocols": [
            "tcp",
        ],
        "operations": [
            "check",
            "wait",
        ],
    }


@router.get(
    "/examples",
    summary="API Examples",
)
async def api_examples():

    return {
        "tcp_check": {
            "method": "POST",
            "endpoint": "/v1/tcp/check",
            "headers": {
                "X-API-Key": "your-api-key",
                "Content-Type": "application/json",
            },
            "request": {
                "host": "google.com",
                "port": 443,
            },
            "response": {
                "reachable": True,
                "elapsed_ms": 13,
                "attempts": 1,
                "message": "Connection successful",
            },
        },
        "tcp_wait": {
            "method": "POST",
            "endpoint": "/v1/tcp/wait",
            "headers": {
                "X-API-Key": "your-api-key",
                "Content-Type": "application/json",
            },
            "request": {
                "host": "10.10.10.20",
                "port": 22,
                "timeout": 300,
                "interval": 2,
            },
        },
    }
