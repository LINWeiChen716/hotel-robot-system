"""接收 Pudu callback（含 notifySwitchMap）並輸出內容。

用法（PowerShell）:
  cd "D:\\SynologyDrive\\桌面\\PYTHON API"
  python .\\切換地圖回調接收.py

可用環境變數:
  PUDU_CALLBACK_HOST (預設 0.0.0.0)
  PUDU_CALLBACK_PORT (預設 8787)
  PUDU_CALLBACK_PATH (預設 /pudu/callback)
"""

from __future__ import annotations

import datetime as dt
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

LOG_DIR = Path("callback_logs")
LOG_FILE = LOG_DIR / "pudu_callbacks.jsonl"

HOST = os.getenv("PUDU_CALLBACK_HOST", "0.0.0.0").strip() or "0.0.0.0"
PORT = int(os.getenv("PUDU_CALLBACK_PORT", "8787"))
CALLBACK_PATH = os.getenv("PUDU_CALLBACK_PATH", "/pudu/callback").strip() or "/pudu/callback"


class CallbackHandler(BaseHTTPRequestHandler):
    server_version = "PuduCallbackServer/1.0"

    def _reply_json(self, status: int, payload: dict) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        # 靜默預設 HTTP 存取日誌，避免干擾回調輸出
        return

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path != CALLBACK_PATH:
            self._reply_json(404, {"message": "not found"})
            return

        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length) if length > 0 else b""

        try:
            payload = json.loads(raw.decode("utf-8") if raw else "{}")
        except Exception:
            payload = {"_raw": raw.decode("utf-8", errors="replace")}

        callback_type = ""
        task_id = ""
        data_obj = payload.get("data") if isinstance(payload, dict) else None
        if isinstance(payload, dict):
            callback_type = str(payload.get("callback_type") or "")
        if isinstance(data_obj, dict):
            task_id = str(data_obj.get("task_id") or "")

        now = dt.datetime.now().isoformat(timespec="seconds")
        entry = {
            "received_at": now,
            "path": path,
            "callback_type": callback_type,
            "task_id": task_id,
            "payload": payload,
        }

        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        print("\n=== callback received ===")
        print(f"time: {now}")
        print(f"callback_type: {callback_type or '(empty)'}")
        print(f"task_id: {task_id or '(empty)'}")
        print(json.dumps(payload, ensure_ascii=False, indent=2))

        # 大多平台只看 200 是否成功
        self._reply_json(200, {"message": "ok"})


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), CallbackHandler)
    url = f"http://{HOST}:{PORT}{CALLBACK_PATH}"
    print("Pudu callback receiver started")
    print(f"listen: {url}")
    print(f"log file: {LOG_FILE}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
