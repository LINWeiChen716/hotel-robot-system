import csv
import datetime as dt
import json
from pathlib import Path
from typing import Any

from services.api_definitions import COMMON_APIS
from services.pudu_client import call_pudu
from services.showroom_service import list_pudu_robots
import services.repo as repo

MAP_NAMES = [
    "1#1#內湖展間v20",
    "1#7#內湖展間清潔v4",
]

PROGRESS_JSONL = Path("reports/api_test_progress.jsonl")
CHECKPOINT_JSON = Path("reports/api_test_checkpoint.json")
LIVE_PROGRESS_MD = Path("reports/api_test_live_progress.md")


def norm_model(s: str) -> str:
    return "".join(ch.lower() for ch in (s or "") if ch.isalnum())


def flatten_apis() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for category, items in COMMON_APIS.items():
        if not isinstance(items, list):
            continue
        for api in items:
            row = dict(api)
            row["category"] = category
            rows.append(row)
    return rows


def set_nested_value(obj: dict[str, Any], dotted_key: str, value: Any) -> None:
    parts = dotted_key.split(".")
    cur = obj
    for part in parts[:-1]:
        child = cur.get(part)
        if not isinstance(child, dict):
            child = {}
            cur[part] = child
        cur = child
    cur[parts[-1]] = value


def parse_example_query(example_value: Any) -> dict[str, Any]:
    if isinstance(example_value, dict):
        return dict(example_value)
    if isinstance(example_value, str):
        out: dict[str, Any] = {}
        for pair in example_value.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                out[k] = v
        return out
    return {}


def parse_example_body(example_value: Any) -> dict[str, Any]:
    if isinstance(example_value, dict):
        return dict(example_value)
    if isinstance(example_value, str):
        try:
            parsed = json.loads(example_value)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            return {}
    return {}


def smart_default_value(key: str, *, sn: str | None, shop_id: int, map_name: str | None, api: dict[str, Any]) -> Any:
    lk = key.lower()
    now = dt.datetime.now()

    if lk in {"sn", "robot_sn", "robotsn", "machine_sn"}:
        return sn or ""
    if lk == "shop_id":
        return shop_id
    if lk == "map_name" or lk.endswith(".map_name"):
        return map_name or MAP_NAMES[0]
    if lk.endswith("point") or lk == "point":
        return "豆豆待機"
    if lk.endswith("point_type") or lk == "point_type":
        return "table"
    if lk == "group_id":
        return 1
    if lk == "device_type":
        return "PuduT300"
    if lk == "task_id":
        return "task-demo-001"
    if lk == "start_date":
        return (now - dt.timedelta(days=7)).strftime("%Y-%m-%d")
    if lk == "end_date":
        return now.strftime("%Y-%m-%d")
    if lk == "limit":
        return 10
    if lk == "offset":
        return 0
    if lk == "volume":
        return 50
    if lk.endswith("is_loop"):
        return False
    if lk.endswith("interval"):
        return 2
    if lk.endswith("times"):
        return 1
    if lk.endswith("qrcode"):
        return "TEST_QRCODE"
    if lk.endswith("urls"):
        return ["https://example.com/demo.png"]
    if lk.endswith("name"):
        action_opts = api.get("action_options")
        if isinstance(action_opts, dict) and action_opts:
            return next(iter(action_opts.keys()))
        return "demo"
    if lk.endswith("action"):
        action_opts = api.get("action_options")
        if isinstance(action_opts, dict) and action_opts:
            return next(iter(action_opts.keys()))
        return "PAUSE"
    return "demo"


def build_params(api: dict[str, Any], *, sn: str | None, shop_id: int, map_name: str | None) -> tuple[dict[str, Any], dict[str, Any]]:
    method = str(api.get("method", "GET")).upper()
    required = dict(api.get("required_params") or {})
    optional = dict(api.get("optional_params") or {})
    examples = dict(api.get("examples") or {})

    query = parse_example_query(examples.get("query"))
    body = parse_example_body(examples.get("body"))

    if method == "GET":
        target = query
    else:
        target = body

    for key in required:
        if key:
            set_nested_value(target, key, smart_default_value(key, sn=sn, shop_id=shop_id, map_name=map_name, api=api))

    # Optional params that are usually safe and useful.
    for key in optional:
        if key in {"shop_id", "map_name", "sn", "limit", "offset", "group_id", "device_type"}:
            set_nested_value(target, key, smart_default_value(key, sn=sn, shop_id=shop_id, map_name=map_name, api=api))

    return query, body


def extract_message(js: Any, text: str) -> str:
    if isinstance(js, dict):
        for k in ("message", "msg", "error_msg", "errorMessage", "desc"):
            v = js.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
    return (text or "").strip()[:200]


def extract_json_success(js: Any) -> str:
    if isinstance(js, dict):
        for k in ("success", "is_success", "ok"):
            if k in js:
                return str(js.get(k))
        if "code" in js:
            return f"code={js.get('code')}"
    return ""


def pick_robots_for_api(api: dict[str, Any], robots: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    supported = api.get("supported_robots") or ["待補充"]
    supported = [str(x) for x in supported]
    supported_norm = {norm_model(x) for x in supported}

    if "all" in supported_norm or "待補充" in supported or not robots:
        return robots, supported

    matched = []
    for rb in robots:
        model = str(rb.get("product_code") or "")
        if norm_model(model) in supported_norm:
            matched.append(rb)
    return matched, supported


def needs_sn(api: dict[str, Any]) -> bool:
    all_keys = list((api.get("required_params") or {}).keys()) + list((api.get("optional_params") or {}).keys())
    return any("sn" in str(k).lower() for k in all_keys)


def needs_map_name(api: dict[str, Any]) -> bool:
    all_keys = list((api.get("required_params") or {}).keys()) + list((api.get("optional_params") or {}).keys())
    path = str(api.get("path") or "")
    return any("map_name" in str(k).lower() for k in all_keys) or "/map-service/" in path


def make_request_key(api: dict[str, Any], *, sn: str | None, map_name: str | None) -> str:
    api_id = str(api.get("id") or "")
    method = str(api.get("method") or "GET").upper()
    path = str(api.get("path") or "")
    return f"{api_id}|{method}|{path}|{sn or ''}|{map_name or ''}"


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_existing_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                if isinstance(item, dict):
                    rows.append(item)
            except json.JSONDecodeError:
                continue
    return rows


def append_live_progress(text: str) -> None:
    LIVE_PROGRESS_MD.parent.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LIVE_PROGRESS_MD.open("a", encoding="utf-8") as f:
        f.write(f"- [{now}] {text}\n")


def write_checkpoint(*, total: int, done: int, pending: int, last_key: str, last_api: str) -> None:
    CHECKPOINT_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated_at": dt.datetime.now().isoformat(),
        "total": total,
        "done": done,
        "pending": pending,
        "last_key": last_key,
        "last_api": last_api,
        "progress_jsonl": str(PROGRESS_JSONL),
        "live_progress_md": str(LIVE_PROGRESS_MD),
    }
    CHECKPOINT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def run() -> None:
    store = repo.get_or_create_default_store()
    shop_id = int(store.get("pudu_shop_id") or 0)
    robots = list_pudu_robots(shop_id) if shop_id else []

    apis = flatten_apis()
    existing_rows = load_existing_rows(PROGRESS_JSONL)
    out_rows: list[dict[str, Any]] = list(existing_rows)
    completed_keys = {str(r.get("request_key") or "") for r in existing_rows if str(r.get("request_key") or "")}

    planned_tasks: list[dict[str, Any]] = []

    for api in apis:
        api_robots, supported_models = pick_robots_for_api(api, robots)

        sn_candidates = [None]
        if needs_sn(api):
            sn_candidates = [r.get("sn") for r in api_robots if r.get("sn")]
            if not sn_candidates:
                planned_tasks.append(
                    {
                        "api": api,
                        "sn": None,
                        "target_model": "",
                        "map_name": None,
                        "supported_models": supported_models,
                        "skip_no_robot": True,
                    }
                )
                continue

        map_candidates = [None]
        if needs_map_name(api):
            map_candidates = MAP_NAMES

        for sn in sn_candidates:
            target_model = ""
            if sn:
                for rb in robots:
                    if rb.get("sn") == sn:
                        target_model = str(rb.get("product_code") or "")
                        break
            for map_name in map_candidates:
                planned_tasks.append(
                    {
                        "api": api,
                        "sn": sn,
                        "target_model": target_model,
                        "map_name": map_name,
                        "supported_models": supported_models,
                        "skip_no_robot": False,
                    }
                )

    total_tasks = len(planned_tasks)
    append_live_progress(f"啟動測試，總任務數: {total_tasks}，已完成(歷史): {len(completed_keys)}")

    done_count = len(completed_keys)

    for task in planned_tasks:
        api = task["api"]
        method = str(api.get("method", "GET")).upper()
        path = str(api.get("path") or "")
        api_id = str(api.get("id") or "")
        api_name = str(api.get("name") or "")
        sn = task["sn"]
        map_name = task["map_name"]
        target_model = task["target_model"]
        supported_models = task["supported_models"]
        request_key = make_request_key(api, sn=sn, map_name=map_name)

        if request_key in completed_keys:
            continue

        current_index = done_count + 1
        append_live_progress(
            f"[{current_index}/{total_tasks}] START {api_id} {method} {path} sn={sn or '-'} map={map_name or '-'}"
        )
        print(f"[PROGRESS] {current_index}/{total_tasks} START {api_id} {method} {path} sn={sn or '-'} map={map_name or '-'}")

        if task["skip_no_robot"]:
            row = {
                "request_key": request_key,
                "category": api.get("category", ""),
                "api_id": api_id,
                "api_name": api_name,
                "method": method,
                "path": path,
                "supported_models": " | ".join(supported_models),
                "target_sn": "",
                "target_model": "",
                "map_name": "",
                "status_code": "SKIP",
                "http_ok": False,
                "message": "No matched robots for supported_models",
                "json_success": "",
                "result_type": "SKIPPED_NO_MATCHED_ROBOT",
            }
        else:
            query, body = build_params(api, sn=sn, shop_id=shop_id, map_name=map_name)

            try:
                resp = call_pudu(method, path, query=query, body=body, timeout=20)
                sc = int(resp.get("status_code") or 0)
                js = resp.get("json")
                txt = str(resp.get("text") or "")
                msg = extract_message(js, txt)
                http_ok = 200 <= sc < 300
                json_success = extract_json_success(js)

                if http_ok and msg.upper() == "SUCCESS":
                    result_type = "OK_MESSAGE_SUCCESS"
                elif http_ok:
                    result_type = "OK_MESSAGE_NOT_SUCCESS"
                else:
                    result_type = "HTTP_ERROR"

                row = {
                    "request_key": request_key,
                    "category": api.get("category", ""),
                    "api_id": api_id,
                    "api_name": api_name,
                    "method": method,
                    "path": path,
                    "supported_models": " | ".join(supported_models),
                    "target_sn": sn or "",
                    "target_model": target_model,
                    "map_name": map_name or "",
                    "status_code": sc,
                    "http_ok": http_ok,
                    "message": msg,
                    "json_success": json_success,
                    "result_type": result_type,
                }
            except Exception as exc:
                row = {
                    "request_key": request_key,
                    "category": api.get("category", ""),
                    "api_id": api_id,
                    "api_name": api_name,
                    "method": method,
                    "path": path,
                    "supported_models": " | ".join(supported_models),
                    "target_sn": sn or "",
                    "target_model": target_model,
                    "map_name": map_name or "",
                    "status_code": "EXCEPTION",
                    "http_ok": False,
                    "message": str(exc),
                    "json_success": "",
                    "result_type": "EXCEPTION",
                }

        out_rows.append(row)
        append_jsonl(PROGRESS_JSONL, row)
        completed_keys.add(request_key)
        done_count += 1
        pending = max(total_tasks - done_count, 0)
        append_live_progress(
            f"[{done_count}/{total_tasks}] DONE {api_id} => {row.get('result_type')} status={row.get('status_code')} message={str(row.get('message') or '')[:80]}"
        )
        print(
            f"[PROGRESS] {done_count}/{total_tasks} DONE {api_id} => {row.get('result_type')} status={row.get('status_code')}"
        )
        write_checkpoint(total=total_tasks, done=done_count, pending=pending, last_key=request_key, last_api=api_id)

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    csv_path = reports_dir / f"api_test_results_{timestamp}.csv"
    md_path = reports_dir / f"api_test_report_{timestamp}.md"

    fieldnames = [
        "request_key",
        "category",
        "api_id",
        "api_name",
        "method",
        "path",
        "supported_models",
        "target_sn",
        "target_model",
        "map_name",
        "status_code",
        "http_ok",
        "message",
        "json_success",
        "result_type",
    ]

    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    total = len(out_rows)
    ok_success = sum(1 for r in out_rows if r["result_type"] == "OK_MESSAGE_SUCCESS")
    ok_not_success = sum(1 for r in out_rows if r["result_type"] == "OK_MESSAGE_NOT_SUCCESS")
    errors = sum(1 for r in out_rows if r["result_type"] in {"HTTP_ERROR", "EXCEPTION"})
    skipped = sum(1 for r in out_rows if r["result_type"] == "SKIPPED_NO_MATCHED_ROBOT")

    issue_rows = [r for r in out_rows if r["result_type"] != "OK_MESSAGE_SUCCESS"]

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# API 全量測試報告\n\n")
        f.write(f"- 產生時間: {dt.datetime.now().isoformat()}\n")
        f.write(f"- Shop ID: {shop_id}\n")
        f.write(f"- 機器人總數: {len(robots)}\n")
        f.write(f"- 地圖測試: {', '.join(MAP_NAMES)}\n")
        f.write(f"- 完整明細 CSV: {csv_path.as_posix()}\n\n")

        f.write("## 統計\n\n")
        f.write("| 指標 | 數量 |\n")
        f.write("|---|---:|\n")
        f.write(f"| 總請求數 | {total} |\n")
        f.write(f"| 成功且 message=SUCCESS | {ok_success} |\n")
        f.write(f"| 成功但 message!=SUCCESS | {ok_not_success} |\n")
        f.write(f"| 失敗（HTTP/Exception） | {errors} |\n")
        f.write(f"| 跳過（無符合型號機器） | {skipped} |\n\n")

        f.write("## 非標準成功與錯誤明細\n\n")
        f.write("| API | Method | SN | 型號 | 地圖 | Status | 類型 | Message |\n")
        f.write("|---|---|---|---|---|---:|---|---|\n")
        for r in issue_rows:
            api_label = f"{r['api_id']} / {r['api_name']}"
            msg = str(r.get("message") or "").replace("\n", " ").replace("|", "\\|")
            f.write(
                f"| {api_label} | {r['method']} | {r['target_sn']} | {r['target_model']} | {r['map_name']} | {r['status_code']} | {r['result_type']} | {msg[:160]} |\n"
            )

    print(json.dumps({
        "csv": str(csv_path),
        "md": str(md_path),
        "total": total,
        "ok_success": ok_success,
        "ok_not_success": ok_not_success,
        "errors": errors,
        "skipped": skipped,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run()
