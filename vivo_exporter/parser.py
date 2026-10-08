#!/usr/bin/env python3

import html
import re

# ============================================================
# HTML PARSER / PARSER HTML
# The modem status page is scraped using regex patterns for the labels in Portuguese.
# A página de status do modem é extraída com padrões regex para os rótulos em português.
# ============================================================


def parse_status(page):
    """
    Parse the modem status page and return the key metrics used by Prometheus.
    Interpreta a página de status do modem e retorna as métricas principais usadas pelo Prometheus.
    """

    result = {}

    # Converte:
    #
    # Pot&ecirc;ncia -> Potência
    #
    page = html.unescape(page)

    normalized = re.sub(
        r"\s+",
        " ",
        page
    )

    # --------------------------------------------------------
    # GPON - LINK
    #
    # <strong>Link:</strong>
    # <br/>
    # Estabelecido
    # --------------------------------------------------------

    match = re.search(
        r"<strong>\s*Link:\s*</strong>"
        r"\s*<br\s*/?>\s*"
        r"([^<]+)",
        normalized,
        re.IGNORECASE
    )

    if match:
        link = match.group(1).strip()
        result["gpon_link"] = (
            link.lower() == "estabelecido"
        )

    # --------------------------------------------------------
    # GPON - RX
    # --------------------------------------------------------

    match = re.search(
        r"<strong>\s*Potência\s+Rx:\s*</strong>"
        r"\s*<br\s*/?>\s*"
        r"([-+]?\d+(?:[.,]\d+)?)\s*dBm",
        normalized,
        re.IGNORECASE
    )

    if match:
        result["rx"] = float(
            match.group(1).replace(",", ".")
        )

    # --------------------------------------------------------
    # GPON - TX
    # --------------------------------------------------------

    match = re.search(
        r"<strong>\s*Potência\s+Tx:\s*</strong>"
        r"\s*<br\s*/?>\s*"
        r"([-+]?\d+(?:[.,]\d+)?)\s*dBm",
        normalized,
        re.IGNORECASE
    )

    if match:
        result["tx"] = float(
            match.group(1).replace(",", ".")
        )

    # --------------------------------------------------------
    # INTERNET - PPP
    #
    # <strong>PPP:</strong>
    # <br/>
    # <span>Conectado</span>
    # --------------------------------------------------------

    match = re.search(
        r"<strong>\s*PPP:\s*</strong>"
        r"\s*<br\s*/?>\s*"
        r"(?:<span[^>]*>)?\s*"
        r"([^<]+)",
        normalized,
        re.IGNORECASE
    )

    if match:
        ppp = match.group(1).strip()
        result["ppp"] = (
            ppp.lower() == "conectado"
        )

    return result
