# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson

from dataclasses import dataclass
from pathlib import Path
import ipaddress
import yaml


CONFIG_FILE = Path(__file__).resolve().parent.parent / "config" / "config.yaml"


@dataclass(frozen=True)
class Application:
    name: str
    version: str


@dataclass(frozen=True)
class Server:
    host: str
    port: int


@dataclass(frozen=True)
class Logging:
    level: str


@dataclass(frozen=True)
class Tcp:
    default_timeout: int
    poll_interval: int


@dataclass(frozen=True)
class Client:
    name: str
    api_key: str


@dataclass(frozen=True)
class Security:
    clients: list[Client]
    allowed_clients: list[ipaddress.IPv4Network]


@dataclass(frozen=True)
class Config:
    application: Application
    server: Server
    logging: Logging
    tcp: Tcp
    security: Security


def load_config() -> Config:

    with CONFIG_FILE.open("r", encoding="utf-8") as fp:
        data = yaml.safe_load(fp)

    return Config(
        application=Application(**data["application"]),
        server=Server(**data["server"]),
        logging=Logging(**data["logging"]),
        tcp=Tcp(**data["tcp"]),
        security=Security(
            clients=[Client(**client) for client in data["security"]["clients"]],
            allowed_clients=[
                ipaddress.ip_network(net) for net in data["security"]["allowed_clients"]
            ],
        ),
    )


config = load_config()
