"""切換地圖測試腳本（switch_map）。

用法（PowerShell）:
  cd "D:\\SynologyDrive\\桌面\\PYTHON API"
  python .\\切換地圖測試.py

可用環境變數覆蓋預設值：
  PUDU_TEST_SN
  PUDU_TEST_MAP_NAME
"""

import json
import os

from dotenv import load_dotenv

from services.pudu_client import call_pudu

load_dotenv()


def main() -> None:
    sn = str(os.getenv("PUDU_TEST_SN", "826094913050022")).strip()
    map_name = os.getenv("PUDU_TEST_MAP_NAME", "0#0#內湖展間v20測試").strip()

    body = {
        "sn": sn,
        "map_info": {
            "map_name": map_name,
        },
    }

    print("=== switch_map request ===")
    print(json.dumps(body, ensure_ascii=False, indent=2))

    result = call_pudu(
        "POST",
        "/open-platform-service/v1/switch_map",
        body=body,
        timeout=20,
        return_raw=True,
    )

    print("\n=== response ===")
    print(f"URL: {result.get('url')}")
    print(f"HTTP: {result.get('status_code')}")

    parsed = result.get("json")
    if parsed is not None:
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
        if isinstance(parsed, dict):
            data = parsed.get("data")
            if isinstance(data, dict) and data.get("task_id"):
                print(f"\nTask ID: {data.get('task_id')}")
    else:
        print(result.get("text", ""))


if __name__ == "__main__":
    main()
