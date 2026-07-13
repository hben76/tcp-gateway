# TCP Gateway v0.2.0

## Overview

Version 0.2.0 represents a significant milestone in the evolution of TCP Gateway. This release expands the service beyond TCP validation into a complete connectivity validation platform supporting TCP, HTTP/HTTPS and ICMP while improving scalability, packaging and overall production readiness.

## Highlights

- Added HTTP and HTTPS connectivity validation
- Added ICMP connectivity validation
- Improved concurrency by eliminating FastAPI event-loop blocking
- Automatic configuration provisioning during installation
- Configurable TCP timeout and polling intervals
- Improved Debian packaging and installation
- General code cleanup and refactoring

---

## Added

### Connectivity

- HTTP connectivity validation endpoint
- HTTPS connectivity validation endpoint
- ICMP connectivity validation endpoint
- Support for configurable TCP timeout and polling interval through `config.yaml`

### Installation

- Automatic creation of `config.yaml` from `config.yaml.example` during installation
- Added `iputils-ping` as a package dependency for ICMP functionality
- Improved first-time installation experience

---

## Changed

### Performance

- Connectivity operations now execute in worker threads, preventing long-running requests from blocking the FastAPI event loop
- Improved handling of concurrent client requests

### Configuration

- TCP timeout and polling interval now default to values defined in `config.yaml`
- Simplified configuration management
- Improved installation defaults

### Project

- Refactored service implementation for improved readability and maintainability
- Improved request and response model consistency
- General code cleanup across the project
- Updated package version to **0.2.0**

---

## Fixed

- Fixed FastAPI event-loop blocking during TCP, HTTP and ICMP wait operations
- Fixed fresh installations where `config.yaml` was not automatically created
- Fixed package dependency required for ICMP connectivity validation
- Fixed timeout handling to correctly use configured default values
- Improved installation reliability on clean systems
- Resolved several issues identified during internal code review

---

## Packaging

- Updated Debian package to version **0.2.0**
- Improved package dependencies
- Improved installation scripts
- Configuration template included in package

---

## Internal Improvements

- Codebase refactoring
- Improved maintainability
- Documentation updates
- Additional automated tests
- General performance optimizations

---

## Supported Protocols

- TCP
- HTTP
- HTTPS
- ICMP

---

## Compatibility

- Ubuntu 24.04 LTS
- Python 3.12+
- systemd
- Debian package installation

---

## Upgrade Notes

Existing installations can be upgraded normally using the Debian package.

For new installations, a default `config.yaml` will now be automatically generated from `config.yaml.example` if one does not already exist.

No configuration changes are required for existing deployments.

---

Thank you to everyone who contributed ideas, testing and code reviews that helped improve the stability and scalability of TCP Gateway.
