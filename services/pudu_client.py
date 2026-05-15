"""Pudu API HMAC 簽名客戶端"""

import base64
import datetime
import hashlib
import hmac
import json
import os
from urllib.parse import quote, unquote, urlparse

import requests
from dotenv import load_dotenv

load_dotenv()


def _build_sign_path(url: str) -> str:
    info = urlparse(url)
    path = info.path or "/"
    if path.startswith(("/release", "/test", "/prepub")):
        path = "/" + path[1:].split("/", 1)[1]
    if info.query:
        split_parts = [p for p in info.query.split("&") if p]
        sorted_query = "&".join(sorted(split_parts))
        # Pudu API gateway expects unquoted query in signing string.
        path = path + "?" + unquote(sorted_query)
    return path


def _make_auth_headers(
    *,
    full_url: str,
    method: str,
    content_md5: str = "",
    accept: str = "application/json",
    content_type: str = "application/json",
    app_key: str = "",
    app_secret: str = "",
) -> dict:
    app_key = app_key or os.getenv("PUDU_APP_KEY", "")
    app_secret = app_secret or os.getenv("PUDU_APP_SECRET", "")
    if app_secret:
        try:
            app_secret = base64.b64decode(app_secret).decode('utf-8')
        except:
            pass  # 如果不是base64，就用原樣
    gmt_format = "%a, %d %b %Y %H:%M:%S GMT"
    x_date = datetime.datetime.now(datetime.UTC).strftime(gmt_format)
    sign_path = _build_sign_path(full_url)
    if method.upper() in ("GET", "HEAD"):
        signing_str = f"x-date: {x_date}\n{method.upper()}\n{accept}\n{content_type}\n{content_md5}\n{sign_path}"
        headers_list = "x-date"
        digestmod = hashlib.sha1
        algorithm = "hmac-sha1"
    else:
        signing_str = f"x-date: {x_date}\n{method.upper()}\n{accept}\n{content_type}\n{content_md5}\n{sign_path}"
        headers_list = "x-date"
        digestmod = hashlib.sha1
        algorithm = "hmac-sha1"
    raw_sign = hmac.new(app_secret.encode(), msg=signing_str.encode(), digestmod=digestmod).digest()
    sign_b64 = base64.b64encode(raw_sign).decode()
    auth = f'hmac id="{app_key}", algorithm="{algorithm}", headers="{headers_list}", signature="{sign_b64}"'
    return {
        "Host": urlparse(full_url).hostname,
        "Accept": accept,
        "Content-Type": content_type,
        "x-date": x_date,
        "Authorization": auth,
    }


def call_pudu(
    method: str,
    doc_path: str,
    *,
    query: dict | None = None,
    body: dict | None = None,
    timeout: int = 20,
    return_raw: bool = False,
) -> dict:
    """
    呼叫 Pudu API。
    doc_path: 不含 /pudu-entry/ 的路徑，例如 /map-service/v1/open/map
              也可以直接傳含 /pudu-entry/ 的完整路徑。
    return_raw: 若為 True，額外回傳 sign_str / authorization / x_date（供 debug）。
    回傳: {"status_code": int, "json": dict|None, "text": str, "url": str}
    """
    hostname = os.getenv("PUDU_HOSTNAME", "css-open-platform.pudutech.com")
    base_url = f"https://{hostname}"

    # 統一加 /pudu-entry/ 前綴
    if not doc_path.startswith("/pudu-entry/"):
        api_path = "/pudu-entry" + doc_path
    else:
        api_path = doc_path

    # 組 query string（依字典序，與簽名規則對齊）
    encoded_parts = []
    for k, v in sorted((query or {}).items()):
        if v is None:
            continue
        encoded_parts.append(f"{quote(str(k), safe='')}={quote(str(v), safe='')}")
    qs = "&".join(encoded_parts)
    full_url = base_url + api_path + (f"?{qs}" if qs else "")

    body_text: str | None = None
    content_md5 = ""
    if method.upper() not in ("GET", "HEAD"):
        body_text = json.dumps(body or {}, ensure_ascii=False)
        md5_raw = hashlib.md5(body_text.encode("utf-8")).digest()
        content_md5 = base64.b64encode(md5_raw).decode()

    headers = _make_auth_headers(
        full_url=full_url,
        method=method,
        content_md5=content_md5,
    )

    resp = requests.request(
        method=method.upper(),
        url=full_url,
        headers=headers,
        data=body_text,
        timeout=timeout,
    )

    try:
        parsed = resp.json()
    except Exception:
        parsed = None

    result: dict = {
        "url": full_url,
        "status_code": resp.status_code,
        "json": parsed,
        "text": resp.text,
    }

    if return_raw:
        # 附加簽名 debug 資訊
        sign_path = _build_sign_path(full_url)
        result["sign_str"] = f"x-date: {headers.get('x-date', '')}\n{method.upper()}\napplication/json\napplication/json\n{content_md5}\n{sign_path}"
        result["authorization"] = headers.get("Authorization", "")
        result["x_date"] = headers.get("x-date", "")

    return result


def request_with_sign(
    base_url: str,
    path: str,
    method: str,
    app_key: str,
    app_secret: str,
    query: dict | None = None,
    body: dict | None = None,
    accept: str = "application/json",
    content_type: str = "application/json",
    language: str = "zh-CN",
    timeout: int = 20,
) -> dict:
    """自訂 base_url 版本，供 API 測試頁面使用。"""
    encoded_query = []
    for k, v in (query or {}).items():
        if v is None:
            continue
        encoded_query.append(f"{quote(str(k), safe='')}={quote(str(v), safe='')}")

    qs = "&".join(encoded_query)
    full_url = base_url.rstrip("/") + path + (f"?{qs}" if qs else "")

    body_text: str | None = None
    content_md5 = ""
    if method.upper() in {"POST", "PUT", "PATCH", "DELETE"}:
        body_text = json.dumps(body or {}, sort_keys=True, ensure_ascii=True)
        md5_raw = hashlib.md5(body_text.encode("utf-8")).digest()
        content_md5 = base64.b64encode(md5_raw).decode()

    headers = _make_auth_headers(
        full_url=full_url,
        method=method,
        content_md5=content_md5,
        accept=accept,
        content_type=content_type,
        app_key=app_key,
        app_secret=app_secret,
    )
    if language:
        headers["Language"] = language

    resp = requests.request(
        method=method.upper(),
        url=full_url,
        headers=headers,
        data=body_text,
        timeout=timeout,
    )

    try:
        parsed = resp.json()
    except Exception:
        parsed = None

    return {
        "url": full_url,
        "headers": headers,
        "status_code": resp.status_code,
        "response_headers": dict(resp.headers),
        "json": parsed,
        "text": resp.text,
    }

