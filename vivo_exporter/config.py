#!/usr/bin/env python3

import os
from pathlib import Path

# ============================================================
# CONFIGURATION / CONFIGURAÇÃO
# ============================================================

MODEM = os.getenv(
    "VIVO_MODEM_URL",
    "http://192.168.15.1"
).rstrip("/")

USERNAME = os.getenv(
    "VIVO_USERNAME",
    "admin"
)

PASSWORD = os.getenv(
    "VIVO_PASSWORD"
)

EXPORTER_PORT = int(
    os.getenv(
        "EXPORTER_PORT",
        "9108"
    )
)

POLL_INTERVAL = int(
    os.getenv(
        "POLL_INTERVAL",
        "60"
    )
)

SCRIPT_DIR = Path(__file__).resolve().parent.parent

LOGIN_URL = f"{MODEM}/cgi-bin/login.cgi"
STATUS_URL = f"{MODEM}/cgi-bin/sophia_info.cgi"
