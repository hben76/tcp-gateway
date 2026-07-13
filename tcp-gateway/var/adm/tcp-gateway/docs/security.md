# TCP Gateway Security

## Overview

TCP Gateway is designed to provide controlled connectivity validation for automation platforms.

Security focuses on:

- Authentication
- Authorization
- Network isolation
- Secure configuration handling
- Operational visibility

---

# Authentication

All connectivity APIs require API key authentication.

Required HTTP header:

```http
X-API-Key: <api-key>



Example:
curl -X POST \
http://localhost:59876/v1/tcp/check \
-H "X-API-Key: AAP-secret-key"


Requests without a valid API key are rejected.
Response:
{
  "code":401,
  "message":"Invalid API key"
}

