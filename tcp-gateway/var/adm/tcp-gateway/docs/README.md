# TCP Gateway

Enterprise connectivity validation service.

## Overview

TCP Gateway is a lightweight API service used to validate network connectivity from automation platforms and operational systems.

The service provides a consistent REST API for checking connectivity using multiple protocols.

## Features

- TCP connectivity checks
- HTTP/HTTPS endpoint checks
- ICMP ping checks
- API key authentication
- JSON responses designed for automation
- OpenAPI documentation
- Health and version endpoints

## Supported Protocols

| Protocol | Endpoint | Description |
|----------|----------|-------------|
| TCP | `/v1/tcp/check` | Check TCP port connectivity |
| TCP | `/v1/tcp/wait` | Wait for TCP service availability |
| HTTP | `/v1/http/check` | Check HTTP/HTTPS endpoint |
| HTTP | `/v1/http/wait` | Wait for HTTP endpoint availability |
| ICMP | `/v1/icmp/check` | Perform ICMP ping check |

## Quick Start

Start the service:

```bash
make run
