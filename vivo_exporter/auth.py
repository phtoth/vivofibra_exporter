#!/usr/bin/env python3

import hashlib
import re
import urllib.error
import urllib.parse
import urllib.request
import http.cookiejar

from .config import LOGIN_URL, MODEM, PASSWORD, USERNAME
from .temp_files import LOGIN_PAGE_FILE, LOGIN_RESPONSE_FILE, save_temp_file

# ============================================================
# PASSWORD ENCODING / CODIFICAÇÃO DA SENHA
# The modem expects the password encoded similarly to JavaScript.
# O modem espera que a senha seja codificada de forma semelhante ao JavaScript.
# ============================================================


def encode_password_like_javascript(password):
    """
    Encode the modem password using the same escaping pattern used by the login form.
    Codifica a senha do modem com o mesmo padrão de escape usado no formulário de login.
    """

    encoded = urllib.parse.quote(
        password,
        safe="-_.!~*'()"
    )

    encoded = re.sub(
        r"%[0-9A-F]{2}",
        lambda m: m.group(0).lower(),
        encoded
    )

    return encoded


# ============================================================
# SID / SID
# The login page exposes a dynamic SID used in the MD5 challenge.
# A página de login expõe um SID dinâmico usado no desafio MD5.
# ============================================================


def extract_sid(page):
    """
    Extract the dynamic SID value from the login page.
    Extrai o valor dinâmico do SID da página de login.
    """

    match = re.search(
        r"""var\s+sid\s*=\s*['\"]([^'\"]+)['\"]""",
        page
    )

    if not match:
        raise RuntimeError(
            "SID não encontrado na página de login"
        )

    return match.group(1)


# ============================================================
# HTTP OPENER / ABERTURA HTTP
# Creates a cookie-aware opener that mimics a browser session.
# Cria um opener com cookies que imita uma sessão do navegador.
# ============================================================


def create_opener():
    """
    Create a browser-like HTTP opener with cookies and common headers.
    Cria um opener HTTP com aparência de navegador, cookies e cabeçalhos comuns.
    """

    cookies = http.cookiejar.CookieJar()

    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(
            cookies
        )
    )

    opener.addheaders = [
        (
            "User-Agent",
            "Mozilla/5.0 "
            "(Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 "
            "(KHTML, like Gecko) "
            "Version/27.0 Safari/605.1.15"
        ),
        (
            "Accept",
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
        (
            "Accept-Language",
            "pt-BR,pt;q=0.9,en;q=0.8"
        )
    ]

    return opener, cookies


# ============================================================
# LOGIN / LOGIN
# Perform the modem login flow: fetch the page, extract SID, hash the password, and submit the form.
# Executa o fluxo de login do modem: busca a página, extrai o SID, calcula o hash da senha e envia o formulário.
# ============================================================


def login(opener, cookies):
    """
    Authenticate against the modem using the dynamic SID and MD5 challenge.
    Autentica no modem usando o SID dinâmico e o desafio MD5.
    """

    # --------------------------------------------------------
    # GET login page / GET página de login
    # --------------------------------------------------------

    response = opener.open(
        LOGIN_URL,
        timeout=10
    )

    login_page = response.read().decode(
        "iso-8859-1",
        errors="ignore"
    )

    save_temp_file(
        LOGIN_PAGE_FILE,
        login_page
    )

    # --------------------------------------------------------
    # Dynamic SID / SID dinâmico
    # --------------------------------------------------------

    sid = extract_sid(
        login_page
    )

    # --------------------------------------------------------
    # Password / Senha
    # --------------------------------------------------------

    encoded_password = (
        encode_password_like_javascript(
            PASSWORD
        )
    )

    hash_input = (
        f"{encoded_password}:{sid}"
    )

    password_hash = hashlib.md5(
        hash_input.encode("utf-8")
    ).hexdigest()

    # --------------------------------------------------------
    # POST login / POST do login
    # --------------------------------------------------------

    post_data = urllib.parse.urlencode({
        "Loginuser": USERNAME,
        "LoginPasswordValue": password_hash,
        "acceptLoginIndex": "1"
    }).encode("utf-8")

    request = urllib.request.Request(
        LOGIN_URL,
        data=post_data,
        method="POST"
    )

    request.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded"
    )

    request.add_header(
        "Origin",
        MODEM
    )

    request.add_header(
        "Referer",
        LOGIN_URL
    )

    response = opener.open(
        request,
        timeout=10
    )

    login_response = response.read().decode(
        "iso-8859-1",
        errors="ignore"
    )

    # --------------------------------------------------------
    # Save login response temporarily / Salva a resposta do login temporariamente
    # --------------------------------------------------------

    save_temp_file(
        LOGIN_RESPONSE_FILE,
        login_response
    )

    # --------------------------------------------------------
    # Session validation / Validação da sessão
    # --------------------------------------------------------

    if len(cookies) == 0:
        raise RuntimeError(
            "Login não criou cookie de sessão"
        )
