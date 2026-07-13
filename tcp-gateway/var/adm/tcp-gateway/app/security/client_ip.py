# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson

import ipaddress

from fastapi import HTTPException, Request, status

from app.config import config


async def verify_client_ip(request: Request) -> str:
    """
    Verify that the client IP is allowed.
    """

    client_ip = ipaddress.ip_address(request.client.host)

    for network in config.security.allowed_clients:
        if client_ip in network:
            return str(client_ip)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Client {client_ip} is not allowed",
    )
