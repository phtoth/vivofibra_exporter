#!/usr/bin/env python3

import threading
import time
import urllib.request

from .auth import create_opener, login
from .config import MODEM, POLL_INTERVAL, STATUS_URL
from .parser import parse_status
from .temp_files import STATUS_RESPONSE_FILE, save_temp_file

# ============================================================
# METRICS STATE / ESTADO DAS MÉTRICAS
# The exporter keeps the latest values synchronized across threads.
# O exporter mantém os últimos valores sincronizados entre threads.
# ============================================================

metrics_lock = threading.Lock()

metrics = {
    "gpon_link": None,
    "rx": None,
    "tx": None,
    "ppp": None,
    "scrape_success": 0,
    "last_success": 0,
}


# ============================================================
# MODEM QUERY / CONSULTA AO MODEM
# Pull the status page from the ONT and extract the metrics used by Prometheus.
# Busca a página de status do ONT e extrai as métricas usadas pelo Prometheus.
# ============================================================


def collect_from_modem():
    """
    Authenticate with the modem and collect the current GPON and PPP status.
    Autentica no modem e coleta o status atual de GPON e PPP.
    """

    opener, cookies = create_opener()

    # --------------------------------------------------------
    # LOGIN / LOGIN
    # --------------------------------------------------------

    login(
        opener,
        cookies
    )

    # --------------------------------------------------------
    # STATUS / STATUS
    # --------------------------------------------------------

    request = urllib.request.Request(
        STATUS_URL
    )

    request.add_header(
        "Referer",
        f"{MODEM}/cgi-bin/sophia_index.cgi"
    )

    response = opener.open(
        request,
        timeout=15
    )

    page = response.read().decode(
        "iso-8859-1",
        errors="ignore"
    )

    # --------------------------------------------------------
    # Save response temporarily / Salva a resposta temporariamente
    # --------------------------------------------------------

    save_temp_file(
        STATUS_RESPONSE_FILE,
        page
    )

    # --------------------------------------------------------
    # PARSER / PARSER
    # --------------------------------------------------------

    result = parse_status(page)

    required = [
        "gpon_link",
        "rx",
        "tx",
        "ppp"
    ]

    missing = [
        field
        for field in required
        if field not in result
    ]

    if missing:
        raise RuntimeError(
            "Campos não encontrados: "
            + ", ".join(missing)
        )

    return result


# ============================================================
# UPDATE METRICS / ATUALIZAR MÉTRICAS
# Refresh the in-memory metrics used by the Prometheus endpoint.
# Atualiza as métricas em memória usadas pelo endpoint do Prometheus.
# ============================================================


def update_metrics():
    """
    Collect modem data and store the latest values in the shared metrics dictionary.
    Coleta dados do modem e armazena os valores mais recentes no dicionário compartilhado de métricas.
    """

    try:
        result = collect_from_modem()

        with metrics_lock:
            metrics["gpon_link"] = (
                1
                if result["gpon_link"]
                else 0
            )

            metrics["rx"] = result["rx"]
            metrics["tx"] = result["tx"]
            metrics["ppp"] = (
                1
                if result["ppp"]
                else 0
            )
            metrics["scrape_success"] = 1
            metrics["last_success"] = int(
                time.time()
            )

        print(
            "[OK] "
            f"GPON={'UP' if result['gpon_link'] else 'DOWN'} "
            f"RX={result['rx']:.2f}dBm "
            f"TX={result['tx']:.2f}dBm "
            f"PPP={'UP' if result['ppp'] else 'DOWN'}"
        )

    except Exception as e:
        with metrics_lock:
            metrics["scrape_success"] = 0

        print(
            f"[ERRO] {e}"
        )


# ============================================================
# COLLECTION LOOP / LOOP DE COLETA
# This thread runs in the background and keeps metrics updated periodically.
# Este thread roda em segundo plano e mantém as métricas atualizadas periodicamente.
# ============================================================


def collector_loop():
    """
    Endless loop that waits for the poll interval and refreshes the modem data.
    Loop infinito que espera o intervalo de polling e atualiza os dados do modem.
    """

    while True:
        time.sleep(POLL_INTERVAL)
        update_metrics()
