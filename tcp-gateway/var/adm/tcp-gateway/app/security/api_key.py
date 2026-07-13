# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# API Key authentication
#

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.config import config

API_KEY_HEADER = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
    description="API key used to authenticate clients.",
)

API_KEYS = {client.api_key: client.name for client in config.security.clients}


async def verify_api_key(
    api_key: str | None = Security(API_KEY_HEADER),
) -> str:
    """
    Verify the supplied API key.

    Returns:
        Client name.
    """

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
        )

    client = API_KEYS.get(api_key)

    if client is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )

    return client
