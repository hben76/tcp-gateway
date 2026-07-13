# SPDX-License-Identifier: AGPL-3.0-only
#
# TCP Gateway
# Copyright (C) 2026 Hans Bengtsson
#
# logger.py
#

import logging
import sys

from app.config import config


def configure_logging() -> logging.Logger:
    """
    Configure the application logger.

    Returns:
        logging.Logger: Configured logger instance.
    """

    logger = logging.getLogger(config.application.name)

    # Prevent duplicate handlers when uvicorn reloads
    if logger.hasHandlers():
        return logger

    logger.setLevel(getattr(logging, config.logging.level.upper(), logging.INFO))

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # Don't pass messages to the root logger
    logger.propagate = False

    return logger
