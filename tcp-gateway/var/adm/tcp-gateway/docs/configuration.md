# TCP Gateway Configuration

## Overview

TCP Gateway configuration is stored in YAML format.

Default configuration file:

```text
config/config.yaml


application:
  name: tcp-gateway
  version: "0.1.0"

server:
  host: 0.0.0.0
  port: 59876

logging:
  level: INFO

tcp:
  default_timeout: 300
  poll_interval: 2

security:
  clients:
    - name: awx
      api_key: awx-secret-key

    - name: airflow
      api_key: airflow-secret-key

  allowed_clients:
    - 127.0.0.1/32
    - 192.168.1.0/24
    - 10.100.0.0/16
