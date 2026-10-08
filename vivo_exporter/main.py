#!/usr/bin/env python3

import threading
from http.server import ThreadingHTTPServer

from .collector import collector_loop, update_metrics
from .config import EXPORTER_PORT, MODEM, PASSWORD, POLL_INTERVAL, SCRIPT_DIR, USERNAME
from .server import MetricsHandler
from .temp_files import cleanup_temp_files

# ============================================================
# MAIN / PRINCIPAL
# Start the exporter, validate the configuration, and keep the HTTP server running.
# Inicia o exporter, valida a configuração e mantém o servidor HTTP em execução.
# ============================================================


def main():
    """
    Entry point for the exporter service.
    Ponto de entrada do serviço do exporter.
    """

    # --------------------------------------------------------
    # Initial cleanup / Limpeza inicial
    # --------------------------------------------------------

    cleanup_temp_files()

    if not PASSWORD:
        print(
            "ERRO: variável VIVO_PASSWORD não definida."
        )
        print()
        print(
            "Exemplo:"
        )
        print(
            "export VIVO_PASSWORD='sua-senha'"
        )
        cleanup_temp_files()
        return

    print()
    print(
        "Vivo Fibra Prometheus Exporter"
    )
    print(
        "--------------------------------"
    )
    print(
        f"Modem:          {MODEM}"
    )
    print(
        f"Usuário:        {USERNAME}"
    )
    print(
        f"Porta:          {EXPORTER_PORT}"
    )
    print(
        f"Intervalo:      {POLL_INTERVAL}s"
    )
    print(
        f"Diretório:      {SCRIPT_DIR}"
    )
    print()

    # --------------------------------------------------------
    # First collection / Primeira coleta
    # --------------------------------------------------------

    update_metrics()

    # --------------------------------------------------------
    # Background collector / Coletor em segundo plano
    # --------------------------------------------------------

    collector = threading.Thread(
        target=collector_loop,
        daemon=True
    )
    collector.start()

    # --------------------------------------------------------
    # HTTP SERVER / SERVIDOR HTTP
    # --------------------------------------------------------

    server = ThreadingHTTPServer(
        (
            "0.0.0.0",
            EXPORTER_PORT
        ),
        MetricsHandler
    )

    print(
        "Exporter disponível em:"
    )
    print(
        f"http://0.0.0.0:{EXPORTER_PORT}/metrics"
    )
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        print(
            "Encerrando exporter..."
        )
    finally:
        # ----------------------------------------------------
        # Stop the server / Para o servidor
        # ----------------------------------------------------
        try:
            server.server_close()
        except Exception:
            pass

        # ----------------------------------------------------
        # Final cleanup / Limpeza final
        # ----------------------------------------------------

        cleanup_temp_files()
        print(
            "Arquivos temporários removidos."
        )


# ============================================================
# ENTRY POINT / PONTO DE ENTRADA
# Run the application when this file is executed directly.
# Executa a aplicação quando este arquivo é executado diretamente.
# ============================================================


if __name__ == "__main__":
    try:
        main()
    finally:
        # Segunda garantia de limpeza.
        # Isso cobre também exceções ocorridas fora do
        # serve_forever().
        cleanup_temp_files()
