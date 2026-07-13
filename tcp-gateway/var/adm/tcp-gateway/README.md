# TCP Gateway

> **Lightweight, protocol-aware connectivity validation for infrastructure automation.**

TCP Gateway is an enterprise-grade REST API that enables automation platforms to validate infrastructure connectivity and service readiness through lightweight, protocol-aware network checks.

Instead of embedding protocol-specific connectivity logic into every automation workflow, TCP Gateway provides a consistent REST interface for verifying that infrastructure services are operational before automation continues.

The gateway is intentionally lightweight and focuses on one responsibility:

> **Determine whether a network service is ready for automation.**

TCP Gateway performs protocol-aware validation without requiring remote command execution, interactive logins or persistent sessions. It is designed to be secure, predictable and easy to deploy in enterprise environments.

Typical use cases include:

* Validate SSH availability after a server reboot.
* Wait for a TCP service to begin accepting connections.
* Verify that a web application is responding after deployment.
* Confirm network connectivity before running Ansible or AWX playbooks.
* Validate infrastructure readiness during CI/CD pipelines.
* Perform health verification from isolated management networks.

TCP Gateway is designed for automation engineers, infrastructure architects, site reliability engineers and cloud platform teams that require fast and reliable connectivity validation.

---

# Why TCP Gateway?

Modern automation platforms frequently need to answer simple but important questions:

* Has the server finished booting?
* Is the SSH service available?
* Is the application accepting HTTP requests?
* Can the service be reached over the network?
* Is the infrastructure ready for the next deployment step?

These checks are often implemented repeatedly across multiple automation platforms, resulting in duplicated code, inconsistent behaviour and unnecessary maintenance.

TCP Gateway centralizes connectivity validation behind a lightweight REST API that provides consistent request and response models regardless of the underlying protocol.

This approach simplifies automation workflows, improves consistency and allows connectivity logic to evolve independently from the automation platform itself.

---

# Key Features

## Connectivity Validation

* TCP connectivity checks
* TCP wait operations
* SSH banner verification
* HTTP connectivity checks
* ICMP connectivity checks

## REST API

* RESTful JSON API
* OpenAPI 3.1 specification
* Swagger UI
* ReDoc documentation
* API discovery endpoint
* Consistent request and response models

## Security

* API key authentication
* Client access control
* Request ID tracking
* Structured request logging
* Secure-by-default design

## Operations

* Health endpoint
* Version endpoint
* Statistics endpoint
* YAML configuration
* systemd integration
* Debian package
* Ubuntu 24.04 LTS support
* Keepalived ready
* UFW friendly

## Engineering

* Python 3.12+
* Modular architecture
* One protocol per service
* Small, maintainable codebase
* Standard library first
* Unit tests
* Performance benchmarks

---

# Design Philosophy

TCP Gateway follows one simple principle:

> **Verify the minimum required to confidently determine that a service is operational.**

Each protocol implements only the validation necessary to determine service readiness.

Examples include:

| Protocol | Validation                      |
| -------- | ------------------------------- |
| TCP      | Successful TCP connection       |
| SSH      | Valid SSH identification banner |
| HTTP     | Valid HTTP response             |
| ICMP     | Successful ICMP Echo Reply      |

By avoiding unnecessary protocol interactions, TCP Gateway remains lightweight, predictable and efficient while providing reliable results for infrastructure automation.


---

# Architecture

TCP Gateway is intentionally designed with a simple, modular architecture.

Each protocol is implemented independently using the same design pattern.

```text
                Automation Platform

      AWX • Ansible • Jenkins • Airflow

                     │
                     ▼

              TCP Gateway REST API

                     │

     ┌───────────────┼────────────────┐
     ▼               ▼                ▼

    TCP             SSH             HTTP

     ▼               ▼                ▼

               ICMP Connectivity

                     │
                     ▼

          Infrastructure & Services
```

Every request follows the same processing pipeline.

```text
Client

    │

    ▼

API Authentication

    │

    ▼

Request Validation

    │

    ▼

Protocol Router

    │

    ▼

Protocol Service

    │

    ▼

Protocol Validation

    │

    ▼

JSON Response
```

This architecture keeps every protocol independent while providing a consistent API for automation platforms.

---

# Project Structure

The project follows a modular layout where every component has a single responsibility.

```text
tcp-gateway/
│
├── app/
│   ├── config/
│   ├── middleware/
│   ├── models/
│   ├── routers/
│   ├── security/
│   ├── services/
│   ├── metadata.py
│   ├── version.py
│   └── main.py
│
├── config/
├── examples/
├── systemd/
├── tests/
│
├── README.md
├── ROADMAP.md
├── LICENSE
├── Makefile
├── pyproject.toml
└── requirements.txt
```

---

# Directory Overview

## app/models

Defines the request and response models used by the REST API.

Each protocol has its own models.

Example:

```text
models/
├── tcp.py
├── ssh.py
├── http.py
└── icmp.py
```

---

## app/routers

Routers expose the REST API endpoints.

Responsibilities include:

* Request validation
* Authentication
* Calling the appropriate service
* Returning JSON responses

Routers contain no protocol-specific logic.

---

## app/services

Services implement the protocol validation logic.

Each service performs one task only.

Example:

```text
services/
├── tcp_service.py
├── ssh_service.py
├── http_service.py
└── icmp_service.py
```

Services are intentionally independent to simplify maintenance and future protocol additions.

---

## app/security

Security components include:

* API Key authentication
* Client validation

Keeping security isolated from business logic makes the project easier to maintain and audit.

---

## app/middleware

Middleware provides cross-cutting functionality including:

* Request IDs
* Request logging
* Exception handling

These features are shared across every API endpoint.

---

## tests

The test suite contains both unit tests and benchmark utilities.

```text
tests/
├── test_tcp.py
├── test_ssh.py
├── test_http.py
├── test_icmp.py
│
├── tcp_benchmark.py
└── ssh_benchmark.py
```

The benchmark scripts provide a simple way to measure throughput and latency under load.

---

# Design Principles

TCP Gateway follows a small set of engineering principles.

## Keep It Simple

Every module has a single responsibility.

Avoid unnecessary abstractions.

Avoid unnecessary dependencies.

Prefer readability over cleverness.

---

## Protocol Aware

TCP Gateway validates the protocol itself rather than simply checking whether a TCP port is open.

Examples:

| Protocol | Validation                      |
| -------- | ------------------------------- |
| TCP      | TCP connection established      |
| SSH      | Valid SSH identification banner |
| HTTP     | Valid HTTP response             |
| ICMP     | Successful Echo Reply           |

This approach provides greater confidence that the service is actually operational.

---

## Stateless

TCP Gateway maintains no client sessions.

Every request is independent.

This simplifies deployment and allows the service to scale horizontally.

---

## Standard Library First

Whenever practical, TCP Gateway uses the Python standard library instead of external dependencies.

Benefits include:

* Smaller deployment footprint
* Faster startup
* Easier maintenance
* Reduced security exposure

External dependencies are introduced only when they provide clear value.

---

## Consistent API

Every protocol follows the same API design.

```
Request

↓

Validation

↓

Service

↓

JSON Response
```

Once an automation platform integrates with one endpoint, every other endpoint behaves in a familiar way.

---

# Supported Protocols

| Protocol         | Check | Wait |   Status  |
| ---------------- | :---: | :--: | :-------: |
| TCP              |   ✅   |   ✅  | Available |
| SSH              |   ✅   |   ❌  | Available |
| HTTP             |   ✅   |   ❌  | Available |
| ICMP             |   ✅   |   ❌  | Available |
| HTTPS            |   🚧  |  🚧  |  Planned  |
| LDAP             |   🚧  |  🚧  |  Planned  |
| DNS              |   🚧  |   ❌  |  Planned  |
| TLS Certificates |   🚧  |   ❌  |  Planned  |

Future protocol support will follow the same architecture and API conventions established by the existing implementations.


---

# Installation

TCP Gateway is distributed as a Debian package and is designed for Ubuntu 24.04 LTS.

## Requirements

| Component        | Version          |
| ---------------- | ---------------- |
| Operating System | Ubuntu 24.04 LTS |
| Python           | 3.12+            |
| systemd          | Required         |
| UFW              | Recommended      |

---

## Install the Debian Package

Install the package using `apt`.

```bash
sudo apt install ./tcp-gateway_0.4.0_amd64.deb
```

Alternatively:

```bash
sudo dpkg -i tcp-gateway_0.4.0_amd64.deb
sudo apt -f install
```

---

## Enable the Service

Enable automatic startup.

```bash
sudo systemctl enable tcp-gateway
```

Start the service.

```bash
sudo systemctl start tcp-gateway
```

Verify the service.

```bash
systemctl status tcp-gateway
```

Expected output:

```text
● tcp-gateway.service - TCP Gateway REST API
     Loaded: loaded
     Active: active (running)
```

---

# Directory Layout

After installation the package installs the following files.

```text
/etc/tcp-gateway/
    config.yaml

/var/adm/tcp-gateway/
    app/
    tests/
    requirements.txt
    README.md

/etc/systemd/system/
    tcp-gateway.service
```

---

# Configuration

The default configuration file is:

```text
/etc/tcp-gateway/config.yaml
```

Example configuration:

```yaml
application:
  name: tcp-gateway
  version: "0.4.0"

server:
  host: 0.0.0.0
  port: 59876

logging:
  level: INFO

security:
  api_keys:
    - name: awx
      key: your-secret-api-key

  allowed_clients:
    - 192.168.1.0/24
```

---

# Configuration Options

## Application

| Parameter | Description         |
| --------- | ------------------- |
| name      | Application name    |
| version   | Application version |

---

## Server

| Parameter | Description        |
| --------- | ------------------ |
| host      | Listening address  |
| port      | TCP listening port |

Example:

```yaml
server:
  host: 0.0.0.0
  port: 59876
```

---

## Logging

Supported logging levels:

* DEBUG
* INFO
* WARNING
* ERROR
* CRITICAL

Example:

```yaml
logging:
  level: INFO
```

---

## Security

API keys are defined in the configuration file.

Example:

```yaml
security:
  api_keys:
    - name: awx
      key: your-secret-key
```

Restrict access to trusted management networks.

Example:

```yaml
allowed_clients:
    - 10.10.0.0/16
    - 192.168.100.0/24
```

---

# Starting the Service

Start the gateway.

```bash
sudo systemctl start tcp-gateway
```

Restart after configuration changes.

```bash
sudo systemctl restart tcp-gateway
```

Stop the service.

```bash
sudo systemctl stop tcp-gateway
```

Restart automatically after boot.

```bash
sudo systemctl enable tcp-gateway
```

Disable automatic startup.

```bash
sudo systemctl disable tcp-gateway
```

---

# Verifying the Installation

Verify that the API is responding.

Health endpoint:

```bash
curl http://localhost:59876/health
```

Example response:

```json
{
    "status": "UP"
}
```

Verify the version.

```bash
curl http://localhost:59876/version
```

Example response:

```json
{
    "version": "0.4.0"
}
```

Verify runtime statistics.

```bash
curl http://localhost:59876/stats
```

Open the interactive API documentation.

```text
http://localhost:59876/api/docs
```

Open the ReDoc documentation.

```text
http://localhost:59876/api/redoc
```

---

# Firewall Configuration

If UFW is enabled, allow access to the configured TCP Gateway port.

Example:

```bash
sudo ufw allow 59876/tcp
```

Verify the firewall configuration.

```bash
sudo ufw status
```

---

# Updating TCP Gateway

Install a newer package using the same installation procedure.

```bash
sudo apt install ./tcp-gateway_0.5.0_amd64.deb
```

The existing configuration file is preserved during package upgrades.

After upgrading, restart the service.

```bash
sudo systemctl restart tcp-gateway
```

Verify the running version.

```bash
curl http://localhost:59876/version
```
---

# REST API

TCP Gateway exposes a RESTful JSON API that is designed to be simple, consistent and automation-friendly.

All protocol endpoints follow the same request and response patterns, making it easy to integrate with automation platforms such as AWX, Ansible, Jenkins, Airflow and custom orchestration systems.

Unless otherwise noted, all API requests use:

* HTTP POST
* JSON request body
* JSON response
* API Key authentication

---

# Authentication

Every protected endpoint requires an API key.

The API key is supplied using the HTTP header:

```text
X-API-Key
```

Example:

```bash
-H "X-API-Key: your-secret-api-key"
```

If authentication fails, the API returns:

```http
HTTP/1.1 401 Unauthorized
```

Example response:

```json
{
    "detail": "Invalid API key."
}
```

---

# Content Type

Requests must specify:

```http
Content-Type: application/json
```

---

# API Overview

## Public Endpoints

| Method | Endpoint            | Description           |
| ------ | ------------------- | --------------------- |
| GET    | `/health`           | Service health        |
| GET    | `/version`          | Application version   |
| GET    | `/stats`            | Runtime statistics    |
| GET    | `/api`              | API discovery         |
| GET    | `/api/info`         | Gateway information   |
| GET    | `/api/examples`     | Example requests      |
| GET    | `/api/docs`         | Swagger UI            |
| GET    | `/api/redoc`        | ReDoc                 |
| GET    | `/api/openapi.json` | OpenAPI specification |

---

## TCP

| Method | Endpoint        | Description                              |
| ------ | --------------- | ---------------------------------------- |
| POST   | `/v1/tcp/check` | Verify TCP connectivity                  |
| POST   | `/v1/tcp/wait`  | Wait until TCP connectivity is available |

---

## SSH

| Method | Endpoint        | Description                                                 |
| ------ | --------------- | ----------------------------------------------------------- |
| POST   | `/v1/ssh/check` | Verify SSH service by reading the SSH identification banner |

---

## HTTP

| Method | Endpoint         | Description              |
| ------ | ---------------- | ------------------------ |
| POST   | `/v1/http/check` | Verify HTTP connectivity |

---

## ICMP

| Method | Endpoint         | Description                                      |
| ------ | ---------------- | ------------------------------------------------ |
| POST   | `/v1/icmp/check` | Verify host reachability using ICMP Echo Request |

---

# Response Format

Every protocol returns a consistent JSON response.

Successful example:

```json
{
    "reachable": true,
    "response_time_ms": 12
}
```

Failed example:

```json
{
    "reachable": false,
    "response_time_ms": 5000,
    "message": "Connection timed out."
}
```

Protocol-specific fields may be included.

Example:

```json
{
    "reachable": true,
    "response_time_ms": 4,
    "ssh_banner": "SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13"
}
```

---

# Error Responses

TCP Gateway returns standard HTTP status codes.

| Status | Description                    |
| ------ | ------------------------------ |
| 200    | Request completed successfully |
| 400    | Invalid request                |
| 401    | Authentication failed          |
| 404    | Endpoint not found             |
| 422    | Request validation failed      |
| 500    | Internal server error          |

---

# Request Validation

Input is validated before protocol processing begins.

Examples include:

* Invalid IP addresses
* Invalid hostnames
* Invalid TCP ports
* Missing required fields
* Incorrect data types

Validation failures return:

```http
422 Unprocessable Entity
```

Example:

```json
{
    "detail": [
        {
            "loc": [
                "body",
                "port"
            ],
            "msg": "Input should be less than or equal to 65535"
        }
    ]
}
```

---

# API Versioning

The REST API uses versioned endpoints.

Current version:

```text
/v1/
```

Example:

```text
/v1/tcp/check
```

Future API versions will be introduced without breaking existing clients whenever practical.

---

# API Design Principles

Every endpoint follows the same lifecycle.

```text
Client

    │

    ▼

Authenticate

    │

    ▼

Validate Request

    │

    ▼

Protocol Service

    │

    ▼

Protocol Validation

    │

    ▼

JSON Response
```

The goal is consistency.

Once an automation platform integrates with one endpoint, every other endpoint behaves in the same way.

---

# Interactive Documentation

TCP Gateway automatically generates OpenAPI documentation.

Swagger UI:

```text
http://localhost:59876/api/docs
```

ReDoc:

```text
http://localhost:59876/api/redoc
```

OpenAPI Specification:

```text
http://localhost:59876/api/openapi.json
```

Example response:

```json
{
    "reachable": true,
    "response_time_ms": 7,
    "ssh_banner": "SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13"
}
```

---

# HTTP Connectivity Check

Verify that a web application is responding.

```bash
curl \
    -X POST http://localhost:59876/v1/http/check \
    -H "X-API-Key: your-secret-api-key" \
    -H "Content-Type: application/json" \
    -d '{
        "url":"https://example.com"
    }'
```

---

# ICMP Connectivity Check

Verify host reachability using ICMP.

```bash
curl \
    -X POST http://localhost:59876/v1/icmp/check \
    -H "X-API-Key: your-secret-api-key" \
    -H "Content-Type: application/json" \
    -d '{
        "host":"192.168.1.100"
    }'
```

---

# Python Example

```python
import requests

response = requests.post(
    "http://localhost:59876/v1/ssh/check",
    headers={
        "X-API-Key": "your-secret-api-key",
    },
    json={
        "host": "server01.example.com",
        "port": 22,
    },
)

print(response.json())
```

---

# Ansible Example

```yaml
- name: Verify SSH service
  uri:
    url: http://gateway:59876/v1/ssh/check
    method: POST
    headers:
      X-API-Key: "{{ gateway_api_key }}"
    body_format: json
    body:
      host: "{{ inventory_hostname }}"
      port: 22
  register: ssh_status

- debug:
    var: ssh_status.json
```

---

# Jenkins Pipeline

```groovy
def response = httpRequest(
    httpMode: 'POST',
    url: 'http://gateway:59876/v1/tcp/check',
    customHeaders: [
        [name: 'X-API-Key', value: credentials('gateway-key')]
    ],
    requestBody: '''
{
    "host":"server01",
    "port":22
}
'''
)

echo response.content
```

---

# Typical Deployment Workflow

A common deployment sequence using TCP Gateway.

```text
Provision Virtual Machine
           │
           ▼
Wait for TCP Connectivity
           │
           ▼
Verify SSH Banner
           │
           ▼
Run Ansible Playbook
           │
           ▼
Verify HTTP Service
           │
           ▼
Deployment Complete
```

---

# Typical Reboot Workflow

```text
Reboot Server
      │
      ▼
TCP Wait
      │
      ▼
SSH Banner Check
      │
      ▼
Continue Automation
```

---

# Best Practices

For reliable automation:

* Use the `/wait` endpoints when waiting for services to become available.
* Use protocol-specific endpoints instead of generic TCP checks whenever possible.
* Restrict API access to trusted management networks.
* Store API keys securely using your automation platform's secret management features.
* Use the `/health` endpoint for monitoring the gateway itself.
* Use the `/stats` endpoint to monitor request volume and connectivity trends.

---

# Additional Examples

The repository contains additional examples for common automation platforms.

```text
examples/
├── curl/
├── python/
├── ansible/
├── awx/
├── airflow/
├── jenkins/
└── postman/


---

# Development

TCP Gateway is designed to be simple to build, test and maintain.

The project follows a modular architecture where each protocol is implemented independently while exposing a consistent REST API.

---

# Development Requirements

| Component | Version   |
| --------- | --------- |
| Ubuntu    | 24.04 LTS |
| Python    | 3.12+     |
| Git       | Current   |
| Ruff      | Latest    |

---

# Clone the Repository

```bash
git clone https://github.com/<your-org>/tcp-gateway.git

cd tcp-gateway
```

---

# Install Dependencies

Create a virtual environment.

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Running the Gateway

Start the development server.

```bash
make run
```

or

```bash
python3 -m uvicorn app.main:app
```

The gateway will start using the configured host and port.

---

# Formatting

TCP Gateway uses Ruff for formatting.

Format the project.

```bash
ruff format .
```

Verify formatting.

```bash
ruff format --check .
```

---

# Linting

Run static analysis.

```bash
ruff check .
```

All commits should pass Ruff without warnings.

---

# Unit Tests

Execute the complete test suite.

```bash
pytest -v
```

Run a single test.

```bash
pytest tests/test_tcp.py -v
```

---

# Performance Benchmarks

TCP Gateway includes benchmark utilities for measuring throughput and latency.

TCP benchmark.

```bash
python3 tests/tcp_benchmark.py \
    --url http://localhost:59876 \
    --name awx \
    --apikey your-secret-api-key
```

SSH benchmark.

```bash
python3 tests/ssh_benchmark.py \
    --url http://localhost:59876 \
    --name awx \
    --apikey your-secret-api-key
```

Typical benchmark output.

```text
============================================================
Benchmark Results
============================================================

Completed     : 1000
Successful    : 1000
Failed        : 0
Duration      : 2.14 s
Requests/sec  : 467.28

Latency

Minimum       : 2.40 ms
Average       : 5.73 ms
Median        : 4.88 ms
Maximum       : 18.61 ms
```

---

# Release Checklist

Before creating a release, verify the following.

## Code Quality

```text
✓ Ruff formatting
✓ Ruff linting
✓ Unit tests
✓ Manual validation
✓ Benchmarks completed
```

---

## Documentation

```text
✓ README updated
✓ ROADMAP updated
✓ Version updated
✓ API documentation verified
```

---

## Packaging

```text
✓ Debian package built
✓ Package installed
✓ systemd service verified
✓ Upgrade tested
```

---

# Project Structure

```text
tcp-gateway/
│
├── app/
│   ├── config/
│   ├── middleware/
│   ├── models/
│   ├── routers/
│   ├── security/
│   ├── services/
│   ├── metadata.py
│   ├── version.py
│   └── main.py
│
├── config/
├── examples/
├── systemd/
├── tests/
│
├── README.md
├── ROADMAP.md
├── LICENSE
├── Makefile
├── pyproject.toml
└── requirements.txt
```

---

# Coding Standards

TCP Gateway follows a small number of engineering principles.

* One protocol per router.
* One protocol per service.
* One protocol per request model.
* One protocol per response model.
* Prefer the Python standard library.
* Keep modules small.
* Keep functions small.
* Avoid unnecessary dependencies.
* Maintain consistent API behaviour.

---


