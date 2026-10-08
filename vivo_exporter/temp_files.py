#!/usr/bin/env python3

from .config import SCRIPT_DIR

# ============================================================
# LOCAL DIRECTORY / ARQUIVOS TEMPORÁRIOS
# Local directory and temporary files used for debugging.
# Diretório local e arquivos temporários usados para depuração.
# ============================================================

LOGIN_PAGE_FILE = (
    SCRIPT_DIR / "vivo-login-page.html"
)

LOGIN_RESPONSE_FILE = (
    SCRIPT_DIR / "vivo-login-response.html"
)

STATUS_RESPONSE_FILE = (
    SCRIPT_DIR / "vivo-status.html"
)

TEMP_FILES = [
    LOGIN_PAGE_FILE,
    LOGIN_RESPONSE_FILE,
    STATUS_RESPONSE_FILE,
]


# ============================================================
# ARQUIVOS TEMPORÁRIOS
# ============================================================

def cleanup_temp_files():
    """
    Remove temporary diagnostic files.
    Remove os arquivos temporários utilizados para diagnóstico.
    """

    for file_path in TEMP_FILES:
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            print(
                f"[AVISO] Não foi possível remover "
                f"{file_path.name}: {e}"
            )


def save_temp_file(file_path, content):
    """
    Save HTML content temporarily in the script directory.
    Salva o conteúdo HTML temporariamente no diretório do próprio script.
    """

    try:
        file_path.write_text(
            content,
            encoding="utf-8"
        )
    except Exception as e:
        print(
            f"[AVISO] Não foi possível salvar "
            f"{file_path.name}: {e}"
        )
