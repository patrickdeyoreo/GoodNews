#!/usr/bin/env python3
"""
Provides tools to collect news articles from the web
"""
import os
import logging
import logging.handlers
from . import theguardian

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
SYSLOG_HANDLER = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG_HANDLER.setLevel(logging.DEBUG)

API_CLIENTS = [theguardian.Client]
SOCKET_PATH = './uds_socket'
