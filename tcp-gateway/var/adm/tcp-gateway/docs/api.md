# TCP Gateway API Reference

## Overview

TCP Gateway provides a REST API for connectivity validation.

The API supports:

- TCP connectivity checks
- HTTP/HTTPS endpoint checks
- ICMP ping checks

Base URL:
http://<server>:PORT


API documentation:

- Swagger UI: `/api/docs`
- OpenAPI: `/api/openapi.json`

---

# Authentication

All `/v1/*` endpoints require an API key.

HTTP Header:

```http
X-API-Key: <api-key>


Example
-H "X-API-Key: awx-secret-key"

Invalid authentication:

Response:
{
  "code": 401,
  "message": "Invalid API key"
}


Common Response Format

All connectivity checks return
{
  "status": "success",
  "reachable": true,
  "reason": "success",
  "message": "Connection successful",
  "response_time_ms": 12
}
Health API
GET /health

Checks service availability.

Example:

curl http://localhost:59876/health

Response:

{
  "status": "UP"
}
Version API
GET /version

Returns application version.

Response:

{
  "application": "tcp-gateway",
  "version": "0.1.0"
}
TCP API
POST /v1/tcp/check

Checks if a TCP port is reachable.

Request
{
  "host": "server.example.com",
  "port": 443,
  "timeout": 5
}

Example:

curl -X POST \
http://localhost:59876/v1/tcp/check \
-H "Content-Type: application/json" \
-H "X-API-Key: awx-secret-key" \
-d '{
  "host":"google.com",
  "port":443
}'

Success:

{
  "status": "success",
  "reachable": true,
  "reason": "success",
  "message": "TCP connection established successfully.",
  "response_time_ms": 12
}

Failure:

{
  "status": "error",
  "reachable": false,
  "reason": "connection_refused",
  "message": "The remote host refused the TCP connection.",
  "response_time_ms": 5
}
POST /v1/tcp/wait

Wait until TCP connectivity is available.

Request:

{
  "host": "database.example.com",
  "port": 5432,
  "timeout": 300,
  "interval": 5
}

Response:

{
  "status": "success",
  "reachable": true,
  "reason": "success",
  "message": "TCP connection established successfully.",
  "response_time_ms": 8,
  "elapsed_seconds": 20
}
HTTP API
POST /v1/http/check

Checks HTTP/HTTPS availability.

Request:

{
  "url": "https://example.com",
  "expected_status": 200,
  "timeout": 10
}

Response:

{
  "status": "success",
  "reachable": true,
  "reason": "success",
  "message": "HTTP endpoint returned expected status.",
  "status_code": 200,
  "response_time_ms": 45
}
POST /v1/http/wait

Wait for HTTP endpoint availability.

Request:

{
  "url":"https://example.com",
  "timeout":300,
  "interval":5
}
ICMP API
POST /v1/icmp/check

Performs ICMP ping.

Request:

{
  "host":"8.8.8.8",
  "timeout":5
}

Response:

{
  "status":"success",
  "reachable":true,
  "reason":"success",
  "message":"ICMP ping successful.",
  "response_time_ms":10
}
Error Codes
HTTP Code	Meaning
200	Request completed
401	Invalid API key
422	Invalid request
500	Internal error
Automation Examples
AWX

Example use case:

Run connectivity check
Validate dependency
Continue deployment only if reachable

Example:

- name: Check database availability
  uri:
    url: http://tcp-gateway:59876/v1/tcp/check
    method: POST
    headers:
      X-API-Key: awx-secret-key
    body:
      host: database.example.com
      port: 5432
