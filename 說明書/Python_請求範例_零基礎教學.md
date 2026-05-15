# Pudu API Python 請求教學（零基礎、繁體）


你只要照著做，就可以：

1. 用 Python 呼叫 Pudu API  
2. 瞭解 GET、POST 差在哪  
3. 把 GET 與 POST 寫在同一支程式裡  

---

## 1) 先懂最重要的觀念（白話）

Pudu API 不是隻填網址就能打，還要做「簽名驗證」。  
你會用到兩把金鑰：

- `ApiAppKey`
- `ApiAppSecret`

每次請求前，你的程式都要先把請求內容組成「簽名字串」，再用 `ApiAppSecret` 算出簽名，放進 `Authorization` Header 才能通過。

---

## 2) 你需要準備什麼

### 2.1 跟平臺申請

- `ApiAppKey`
- `ApiAppSecret`
- API 網域（例如 `https://xxxxxx.com`）

### 2.2 電腦安裝

先確認有 Python 3，然後安裝 `requests`：

```powershell
python -m pip install requests
```

---

## 3) GET 與 POST 差在哪（先看懂）

- `GET`：資料通常放在網址後面（Query Params），通常用來「查資料」
- `POST`：資料通常放在 Body（JSON），通常用來「新增/下指令」

你在 Pudu 文件裡看到：

- `請求方法（Method）` = GET 或 POST
- `請求路徑（Path）` = 例如 `/open-platform-service/v2/status/get_by_sn`
- `請求體（Params）` = POST 常見內容

就把這三樣丟進下面的通用函式就可以。

---

## 4) 一支程式同時支援 GET + POST（可直接貼上）

> 說明：這段已把簽名流程包好，給新手直接用。  
> 來源依據：`Pudu_Cloud_API_Docs拷貝.cleaned.md` 中「應用認證 / 簽名生成與傳遞」規則。

```python
# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone
from urllib.parse import urlencode

import requests


# ====== 你要改的設定（先改這裡） ======
BASE_URL = "https://xxxxxx.com"
API_APP_KEY = "Your ApiAppKey"
API_APP_SECRET = "Your ApiAppSecret"
# =====================================


def rfc_1123_gmt_now() -> str:
    """產生 API 常用的 GMT 時間字串"""
    return datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")


def build_content_md5(body_text: str) -> str:
    """
    Content-MD5 = Base64(MD5(body_bytes))
    只有有 body 時才需要，GET 通常留空字串。
    """
    md5_bytes = hashlib.md5(body_text.encode("utf-8")).digest()
    return base64.b64encode(md5_bytes).decode("utf-8")


def build_string_to_sign(
    x_date: str,
    method: str,
    accept: str,
    content_type: str,
    content_md5: str,
    path_and_query: str
) -> str:
    """
    依文件規則組成簽名字串（6 段）
    1) Headers（此範例只簽 x-date）
    2) HTTPMethod
    3) Accept
    4) Content-Type
    5) Content-MD5
    6) PathAndParameters
    """
    headers_part = f"x-date: {x_date}\n"
    lines = [
        headers_part.rstrip("\n"),  # 這行對應 Headers 區塊
        method.upper(),
        accept,
        content_type,
        content_md5,
        path_and_query,
    ]
    return "\n".join(lines)


def build_authorization(string_to_sign: str) -> str:
    """
    Authorization: hmac id="...", algorithm="hmac-sha1", headers="x-date", signature="..."
    """
    digest = hmac.new(
        API_APP_SECRET.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha1,  # 文件示例預設 hmac-sha1
    ).digest()
    signature = base64.b64encode(digest).decode("utf-8")
    return (
        f'hmac id="{API_APP_KEY}", '
        f'algorithm="hmac-sha1", '
        f'headers="x-date", '
        f'signature="{signature}"'
    )


def send_pudu_request(method: str, path: str, query=None, body=None, timeout=30):
    """
    通用請求函式：GET / POST 都走這一支
    - method: "GET" 或 "POST"
    - path: 例如 "/open-platform-service/v2/status/get_by_sn"
    - query: dict，GET 常用
    - body: dict，POST 常用
    """
    query = query or {}
    body = body or {}

    method = method.upper()
    accept = "application/json"
    content_type = "application/json"
    x_date = rfc_1123_gmt_now()

    # 組 URL 與 PathAndParameters
    query_string = urlencode(query, doseq=True)
    path_and_query = f"{path}?{query_string}" if query_string else path
    url = f"{BASE_URL}{path_and_query}"

    # 有 body 才計算 Content-MD5
    if method == "POST":
        body_text = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
        content_md5 = build_content_md5(body_text)
    else:
        body_text = ""
        content_md5 = ""

    # 簽名
    string_to_sign = build_string_to_sign(
        x_date=x_date,
        method=method,
        accept=accept,
        content_type=content_type,
        content_md5=content_md5,
        path_and_query=path_and_query,
    )
    authorization = build_authorization(string_to_sign)

    headers = {
        "Accept": accept,
        "Content-Type": content_type,
        "X-Date": x_date,
        "Authorization": authorization,
    }
    if content_md5:
        headers["Content-MD5"] = content_md5

    # 真正送出
    if method == "GET":
        resp = requests.get(url, headers=headers, timeout=timeout)
    elif method == "POST":
        resp = requests.post(url, headers=headers, data=body_text.encode("utf-8"), timeout=timeout)
    else:
        raise ValueError("只支援 GET / POST")

    return resp


if __name__ == "__main__":
    # ===== 範例 A：GET（查機器狀態）=====
    get_path = "/open-platform-service/v2/status/get_by_sn"
    get_query = {"sn": "SN-PD202405000001"}

    get_resp = send_pudu_request(
        method="GET",
        path=get_path,
        query=get_query,
    )
    print("GET 狀態碼:", get_resp.status_code)
    print("GET 回應:", get_resp.text)

    # ===== 範例 B：POST（播放語音）=====
    post_path = "/open-platform-service/v1/voice/play"
    post_body = {
        "sn": "SN-PD202405000001",
        "voice_id": "10001"
    }

    post_resp = send_pudu_request(
        method="POST",
        path=post_path,
        body=post_body,
    )
    print("POST 狀態碼:", post_resp.status_code)
    print("POST 回應:", post_resp.text)
```

---

## 5) 你之後只要改哪幾個地方

每次換 API，只要改：

1. `method`（GET 或 POST）
2. `path`（文件上的請求路徑）
3. `query`（GET 參數）
4. `body`（POST 參數）

其他簽名程式碼可以不動。

---

## 6) 新手最常犯錯（照這裡排查）

### 錯誤 1：401 / HMAC signature does not match

通常是簽名內容不一致，請檢查：

- `path` 跟 query 組字串是否跟實際請求完全一致
- `X-Date` 是否有帶
- `ApiAppSecret` 是否正確
- `Authorization` 的 `headers="x-date"` 是否一致

### 錯誤 2：沒帶 Accept，簽名失敗

文件有提醒：`Accept` 建議明確設定，避免客戶端自動塞 `*/*` 導致簽名對不起來。

### 錯誤 3：POST 有 body 但沒帶 Content-MD5

若 API gateway 要求 body 驗證，沒帶 `Content-MD5` 可能過不了。  
本文件範例已自動處理 POST 的 `Content-MD5`。

---

## 7) 完全不懂也能照做的操作流程

1. 把上面 Python 程式存成 `pudu_api_demo.py`
2. 把 `BASE_URL`、`API_APP_KEY`、`API_APP_SECRET` 改成你的資料
3. 先只保留 GET 範例，執行一次：

```powershell
python pudu_api_demo.py
```

4. 看到 GET 成功後，再打開 POST 範例測試
5. 之後每新增一支 API，就複製「範例 A/B」區塊改參數即可

---

## 8) 如何把文件裡任一 API 轉成 Python 呼叫

以文件任一章節為例，對照規則：

- `請求方法（Method）` -> `method`
- `請求路徑（Path）` -> `path`
- `請求體（Params）`（若是 GET 通常放 query；若是 POST 放 body）

### 套用範例（GET）

文件：

- `GET /open-platform-service/v2/recharge?sn=SN-PD202405000001`

程式：

```python
resp = send_pudu_request(
    method="GET",
    path="/open-platform-service/v2/recharge",
    query={"sn": "SN-PD202405000001"},
)
```

### 套用範例（POST）

文件：

- `POST /open-platform-service/v1/control_doors`

程式：

```python
resp = send_pudu_request(
    method="POST",
    path="/open-platform-service/v1/control_doors",
    body={"sn": "SN-PD202405000001", "door_action": 1},
)
```

---

## 9) 這份教學對應你原始文件的哪一段

對應來源：`my_project/pudu-robot-control/Pudu_Cloud_API_Docs拷貝.cleaned.md`

- 「Python（應用認證）」
- 「簽名生成和認證流程」
- 「生成與傳遞簽名（Headers / HTTPMethod / Accept / Content-Type / Content-MD5 / PathAndParameters）」

