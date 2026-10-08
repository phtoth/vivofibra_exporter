#!/usr/bin/env python3

# ------------------------------------------------------------
# Vivo Fibra Prometheus Exporter
#
# This is the startup entry point for the project.
# The actual logic is organized in the "vivo_exporter" package
# to keep the code modular and easier to maintain.
#
# Structure:
# - vivo_exporter/config.py     : environment variables and settings
# - vivo_exporter/temp_files.py : temporary HTML/debug file handling
# - vivo_exporter/auth.py       : modem authentication and session login
# - vivo_exporter/parser.py     : HTML parsing of the modem status page
# - vivo_exporter/collector.py  : data collection and metric updates
# - vivo_exporter/prometheus.py : export format for Prometheus scraping
# - vivo_exporter/server.py     : HTTP server for / and /metrics
# - vivo_exporter/main.py       : main execution flow and service startup
#
# Este é o ponto de entrada do projeto.
# A lógica real está organizada no pacote "vivo_exporter"
# para manter o código modular e mais fácil de manter.
#
# Estrutura:
# - vivo_exporter/config.py     : variáveis de ambiente e configurações
# - vivo_exporter/temp_files.py : manipulação de arquivos temporários HTML/debug
# - vivo_exporter/auth.py       : autenticação e login no modem
# - vivo_exporter/parser.py     : parsing do HTML da página de status
# - vivo_exporter/collector.py  : coleta de dados e atualização de métricas
# - vivo_exporter/prometheus.py : formato de exportação para coleta do Prometheus
# - vivo_exporter/server.py     : servidor HTTP para / e /metrics
# - vivo_exporter/main.py       : fluxo principal e inicialização do serviço
# ------------------------------------------------------------

from vivo_exporter.main import main
from vivo_exporter.temp_files import cleanup_temp_files


if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup_temp_files()
