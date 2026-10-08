#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler

from .prometheus import prometheus_output

# ============================================================
# HTTP SERVER / SERVIDOR HTTP
# Expose metrics using a lightweight ThreadingHTTPServer.
# Expõe as métricas usando um ThreadingHTTPServer leve.
# ============================================================


class MetricsHandler(BaseHTTPRequestHandler):
    """
    Minimal HTTP handler for / and /metrics endpoints.
    Manipulador HTTP mínimo para os endpoints / e /metrics.
    """

    def do_GET(self):
        # ----------------------------------------------------
        # /metrics / /metrics
        # ----------------------------------------------------

        if self.path == "/metrics":
            body = prometheus_output().encode("utf-8")

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/plain; version=0.0.4; charset=utf-8"
            )
            self.send_header(
                "Content-Length",
                str(len(body))
            )
            self.end_headers()
            self.wfile.write(body)
            return

        # ----------------------------------------------------
        # / root endpoint / endpoint raiz
        # ----------------------------------------------------

        if self.path == "/":
            body = (
                "Vivo Fibra Prometheus Exporter\n"
                "\n"
                "Metrics: /metrics\n"
            ).encode("utf-8")

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/plain; charset=utf-8"
            )
            self.send_header(
                "Content-Length",
                str(len(body))
            )
            self.end_headers()
            self.wfile.write(body)
            return

        # ----------------------------------------------------
        # 404 Not Found / 404 Não encontrado
        # ----------------------------------------------------

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        return
