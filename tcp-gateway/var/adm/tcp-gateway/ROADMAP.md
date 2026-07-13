# TCP Gateway Roadmap

This document describes the planned evolution of TCP Gateway.

The roadmap may change as the project evolves.

---

# Current Release

## v0.4.0

**Focus:** Multi-Protocol Connectivity

### Completed

- FastAPI framework
- YAML configuration
- API Key authentication
- Request ID middleware
- Request logging middleware
- Global exception handler
- Standard response models
- Health endpoint
- Version endpoint
- Statistics endpoint
- API discovery
- Swagger UI
- ReDoc
- OpenAPI

### Connectivity

- TCP connectivity check
- TCP wait operation
- SSH banner verification
- HTTP connectivity check
- ICMP connectivity check

### Quality

- Unit tests
- TCP benchmark
- SSH benchmark

### Packaging

- Debian package
- systemd service
- Installation guide

---

# Upcoming Releases

## v0.5.0

**Focus:** Service Enhancements

### SSH

- SSH wait operation

### HTTP

- HTTP wait operation

### HTTPS

- HTTPS connectivity check
- HTTPS wait operation

### LDAP

- LDAP connectivity check
- LDAP wait operation

### TLS

- Certificate validation
- Certificate expiration check
- Hostname validation

### Quality

- CI/CD pipeline
- Increased test coverage
- Performance improvements

---

## v1.0.0

**First Stable Release**

### Goals

- Stable REST API
- Complete documentation
- Ubuntu package
- Production ready
- Enterprise quality

---

# Design Principles

TCP Gateway follows these principles.

- Keep the architecture simple.
- One responsibility per module.
- Configuration over hardcoded values.
- Consistent API design.
- Security by default.
- Comprehensive documentation.
- Production-ready quality.

---

# Supported Platform

TCP Gateway targets:

- Ubuntu 24.04 LTS
- Python 3.12+
- systemd
- UFW
- journald

---

# Long-Term Vision

TCP Gateway aims to provide a simple, secure and reliable REST API for infrastructure connectivity validation.

The primary target platforms are automation systems such as:

- AWX
- Ansible
- Airflow
- Jenkins
- Custom automation platforms
