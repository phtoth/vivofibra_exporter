#!/usr/bin/env python3

from .collector import metrics, metrics_lock

# ============================================================
# PROMETHEUS OUTPUT / SAÍDA DO PROMETHEUS
# Build the metrics file with the format expected by Prometheus scrapers.
# Constrói o arquivo de métricas no formato esperado pelos scrapers do Prometheus.
# ============================================================


def prometheus_output():
    """
    Format the current metrics as a Prometheus exposition document.
    Formata as métricas atuais em um documento de exposição do Prometheus.
    """

    with metrics_lock:
        data = metrics.copy()

    lines = []

    # --------------------------------------------------------
    # EXPORTER STATUS / STATUS DO EXPORTER
    # --------------------------------------------------------

    lines.append(
        "# HELP vivo_exporter_scrape_success "
        "Indica se a última coleta do modem foi bem sucedida"
    )
    lines.append(
        "# TYPE vivo_exporter_scrape_success gauge"
    )
    lines.append(
        f"vivo_exporter_scrape_success "
        f"{data['scrape_success']}"
    )

    # --------------------------------------------------------
    # LAST SUCCESSFUL COLLECTION / ÚLTIMA COLETA BEM-SUCEDIDA
    # --------------------------------------------------------

    lines.append(
        "# HELP vivo_exporter_last_success_timestamp_seconds "
        "Timestamp Unix da última coleta bem sucedida"
    )
    lines.append(
        "# TYPE "
        "vivo_exporter_last_success_timestamp_seconds gauge"
    )
    lines.append(
        "vivo_exporter_last_success_timestamp_seconds "
        f"{data['last_success']}"
    )

    # --------------------------------------------------------
    # GPON LINK / LINK GPON
    # --------------------------------------------------------

    if data["gpon_link"] is not None:
        lines.append(
            "# HELP vivo_gpon_link_up "
            "Estado do link GPON "
            "(1=Estabelecido, 0=Não estabelecido)"
        )
        lines.append(
            "# TYPE vivo_gpon_link_up gauge"
        )
        lines.append(
            f"vivo_gpon_link_up "
            f"{data['gpon_link']}"
        )

    # --------------------------------------------------------
    # GPON RX / RX GPON
    # --------------------------------------------------------

    if data["rx"] is not None:
        lines.append(
            "# HELP vivo_gpon_rx_dbm "
            "Potência óptica recebida GPON em dBm"
        )
        lines.append(
            "# TYPE vivo_gpon_rx_dbm gauge"
        )
        lines.append(
            f"vivo_gpon_rx_dbm "
            f"{data['rx']}"
        )

    # --------------------------------------------------------
    # GPON TX / TX GPON
    # --------------------------------------------------------

    if data["tx"] is not None:
        lines.append(
            "# HELP vivo_gpon_tx_dbm "
            "Potência óptica transmitida GPON em dBm"
        )
        lines.append(
            "# TYPE vivo_gpon_tx_dbm gauge"
        )
        lines.append(
            f"vivo_gpon_tx_dbm "
            f"{data['tx']}"
        )

    # --------------------------------------------------------
    # PPP / PPP
    # --------------------------------------------------------

    if data["ppp"] is not None:
        lines.append(
            "# HELP vivo_ppp_connected "
            "Estado da conexão PPP "
            "(1=Conectado, 0=Desconectado)"
        )
        lines.append(
            "# TYPE vivo_ppp_connected gauge"
        )
        lines.append(
            f"vivo_ppp_connected "
            f"{data['ppp']}"
        )

    return "\n".join(lines) + "\n"
