"""
Showroom 業務邏輯（對應 Next.js 版的 lib/showroom/service.ts）
- 模板 token 解析
- 按鈕執行（對每臺機器人依序呼叫 action templates）
- 機器人狀態輪詢
- 地圖快照取得
"""

from __future__ import annotations

import datetime
import json
import re
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import parse_qs, urlparse

from services.pudu_client import call_pudu


# ─────────────────────────── Token 解析 ───────────────────────────

_TOKEN_RE = re.compile(r"\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}")
_DATE_RE = re.compile(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})")


def _to_unix_ts(date_str: str, *, end_of_day: bool, tz_offset_hours: int) -> int | None:
    m = _DATE_RE.fullmatch((date_str or "").strip())
    if not m:
        return None
    y, mm, dd = int(m.group(1)), int(m.group(2)), int(m.group(3))
    try:
        tz = datetime.timezone(datetime.timedelta(hours=tz_offset_hours))
        if end_of_day:
            dt = datetime.datetime(y, mm, dd, 23, 59, 59, tzinfo=tz)
        else:
            dt = datetime.datetime(y, mm, dd, 0, 0, 0, tzinfo=tz)
        return int(dt.timestamp())
    except Exception:
        return None


def _coerce_timezone_offset(value: object) -> int:
    try:
        return int(str(value).strip())
    except Exception:
        return 0


def _get_timezone_offset_hours(query: dict | None, body: dict | None) -> int:
    for src in (query, body):
        if isinstance(src, dict) and "timezone_offset" in src:
            return _coerce_timezone_offset(src.get("timezone_offset"))
    return 0


def _convert_time_fields_inplace(obj: object, *, tz_offset_hours: int) -> None:
    if isinstance(obj, dict):
        for key, value in list(obj.items()):
            if key in ("start_time", "end_time") and isinstance(value, str):
                ts = _to_unix_ts(
                    value,
                    end_of_day=(key == "end_time"),
                    tz_offset_hours=tz_offset_hours,
                )
                if ts is not None:
                    obj[key] = ts
            else:
                _convert_time_fields_inplace(value, tz_offset_hours=tz_offset_hours)
    elif isinstance(obj, list):
        for item in obj:
            _convert_time_fields_inplace(item, tz_offset_hours=tz_offset_hours)


def _resolve_token(token: str, context: dict) -> str | None:
    now = datetime.datetime.now(datetime.UTC)
    mapping = {
        "robot.sn": context.get("robot", {}).get("sn", ""),
        "robot.nickname": context.get("robot", {}).get("nickname", "") or "",
        "store.pudu_shop_id": str(context.get("store", {}).get("pudu_shop_id", "")),
        "store.name": context.get("store", {}).get("name", ""),
        "group.name": context.get("group", {}).get("name", ""),
        "now.ms": str(int(now.timestamp() * 1000)),
        "now.s": str(int(now.timestamp())),
        "now.iso": now.isoformat(),
    }
    return mapping.get(token)


def resolve_template(value: object, context: dict) -> object:
    """遞迴解析 {{token}} 佔位符"""
    if isinstance(value, str):
        def replace(m: re.Match) -> str:
            resolved = _resolve_token(m.group(1).strip(), context)
            return resolved if resolved is not None else m.group(0)
        return _TOKEN_RE.sub(replace, value)
    if isinstance(value, dict):
        return {k: resolve_template(v, context) for k, v in value.items()}
    if isinstance(value, list):
        return [resolve_template(item, context) for item in value]
    return value


# ─────────────────────────── 按鈕執行 ───────────────────────────

def _literal_sn_from_body_dict(body: dict) -> str | None:
    """從未套用 context 的 body_template 中取出『純文字』SN（不含 {{ 佔位符）。"""
    for key in ("sn", "SN", "Sn", "robot_sn", "robotSn", "machine_sn", "robot_id"):
        v = body.get(key)
        if isinstance(v, str):
            s = v.strip()
            if s and "{{" not in s:
                return s
    for nested_key in ("data", "payload", "map_info", "mapInfo", "robot_info", "robotInfo", "robot"):
        sub = body.get(nested_key)
        if isinstance(sub, dict):
            for key in ("sn", "SN", "Sn", "robot_sn", "robotSn", "machine_sn"):
                v = sub.get(key)
                if isinstance(v, str):
                    s = v.strip()
                    if s and "{{" not in s:
                        return s
    return None


def _load_json_object(value: object) -> dict | None:
    """若模板欄位是 JSON 字串，嘗試轉成 dict。"""
    if isinstance(value, dict):
        return value
    if not isinstance(value, str):
        return None
    s = value.strip()
    if not s:
        return None
    try:
        parsed = json.loads(s)
    except Exception:
        return None
    return parsed if isinstance(parsed, dict) else None


def _extract_sn_from_path(path: object) -> str | None:
    """從 path（含 querystring 或完整 URL）擷取固定 SN。"""
    if not isinstance(path, str):
        return None
    raw = path.strip()
    if not raw:
        return None
    parsed = urlparse(raw)
    q = parse_qs(parsed.query, keep_blank_values=False)
    for key in ("sn", "robot_sn", "robotSn", "machine_sn", "robot_id"):
        values = q.get(key) or []
        for v in values:
            s = str(v).strip()
            if s and "{{" not in s:
                return s
    return None


def _unwrap_template_payload_obj(obj: dict) -> dict:
    """
    相容舊資料：body/query 可能誤存成整包 action payload（含 bodyTemplate/queryTemplate）。
    優先回傳真正可送出的 payload dict。
    """
    for key in ("bodyTemplate", "body_template", "payload", "data"):
        nested = obj.get(key)
        if isinstance(nested, dict):
            return nested
    return obj


def _extract_query_template_obj(value: object) -> dict:
    """取得真正 query template（支援舊資料包裝格式）。"""
    obj = _load_json_object(value)
    if obj is None:
        return {}
    for key in ("queryTemplate", "query_template"):
        nested = obj.get(key)
        if isinstance(nested, dict):
            return nested
    return obj


def _extract_body_template_obj(value: object) -> dict:
    """取得真正 body template（支援舊資料包裝格式）。"""
    obj = _load_json_object(value)
    if obj is None:
        return {}
    return _unwrap_template_payload_obj(obj)


def _normalize_template_obj(value: object, context: dict) -> dict:
    """
    允許 query/body template 來源是 dict 或 JSON 字串，並套用 token replace。
    """
    obj = _load_json_object(value)
    if obj is None:
        return {}
    resolved = resolve_template(obj, context)
    return resolved if isinstance(resolved, dict) else {}


def resolve_literal_target_sn(template: dict) -> str | None:
    """
    判斷此範本是否『只對單一 SN』執行一次。

    優先順序：
    1. 資料庫欄位 fixed_robot_sn
    2. Body Template JSON 裡的純文字 sn（及常見巢狀）
    3. Query Template JSON 的 sn 參數

    若 body 使用 {{robot.sn}} 等佔位符，無法推斷固定 SN，回傳 None（走舊：對每臺勾選機器人各跑一次）。
    """
    explicit = (template.get("fixed_robot_sn") or "").strip()
    if explicit:
        return explicit
    body = _extract_body_template_obj(template.get("body_template"))
    if body:
        sn = _literal_sn_from_body_dict(body)
        if sn:
            return sn
    query = _extract_query_template_obj(template.get("query_template"))
    if query:
        v = query.get("sn")
        if isinstance(v, str):
            s = v.strip()
            if s and "{{" not in s:
                return s
    sn_in_path = _extract_sn_from_path(template.get("path"))
    if sn_in_path:
        return sn_in_path
    return None


def _run_action(template: dict, context: dict) -> dict:
    method = template.get("method", "GET")
    path = template.get("path", "")
    timeout_ms = template.get("timeout_ms") or 15000
    timeout_sec = max(1, timeout_ms // 1000)

    query_raw = _normalize_template_obj(_extract_query_template_obj(template.get("query_template")), context)
    body_raw = _normalize_template_obj(_extract_body_template_obj(template.get("body_template")), context)

    query = {k: v for k, v in query_raw.items() if v not in (None, "")}
    body = body_raw

    tz_offset_hours = _get_timezone_offset_hours(query, body)
    _convert_time_fields_inplace(query, tz_offset_hours=tz_offset_hours)
    _convert_time_fields_inplace(body, tz_offset_hours=tz_offset_hours)

    start = time.monotonic()
    ok = False
    status_code = 0
    resp_text = ""
    request_url = ""
    resp_json: dict | list | None = None
    try:
        result = call_pudu(method, path, query=query, body=body, timeout=timeout_sec)
        ok = 200 <= result["status_code"] < 300
        status_code = result["status_code"]
        request_url = str(result.get("url") or "")
        resp_text = result.get("text") or ""
        resp_json = result.get("json")
    except Exception as exc:
        resp_text = str(exc)

    elapsed = int((time.monotonic() - start) * 1000)
    return {
        "actionId": template.get("id", ""),
        "actionName": template.get("name", ""),
        "method": method,
        "path": path,
        "requestUrl": request_url,
        "requestQuery": query,
        "requestBody": body,
        "ok": ok,
        "status": status_code,
        "elapsedMs": elapsed,
        "responseBody": resp_text,
        "responseJson": resp_json,
    }


def execute_button(
    button: dict,
    robots: list[dict],
    store: dict,
    group: dict | None = None,
) -> dict:
    """
    執行 button 底下的 actions。

    - 若範本可判定『只對單一 SN』（**fixed_robot_sn** 或 **Body／Query Template 內純文字 sn**）：
      只對該 SN 打一次，且僅當操作頁有勾選該臺（在傳入的 robots 內）才執行。
    - 若此按鈕**每一個**啟用範本都能解析出固定 SN：會先將勾選清單與「範本裡出現的 SN 聯集」取交集——
      勾到按鈕裡沒有任何範本對應的機器人會直接略過（不發請求）。
    - 若有任一範本無法解析固定 SN（例如 body 仍用 {{robot.sn}}）：維持舊行為，對傳入的每臺機器人各執行該範本。
    """
    started_at = datetime.datetime.now(datetime.UTC).isoformat()

    actions = sorted(button.get("actions", []), key=lambda a: a.get("action_order", 0))
    enabled_templates: list[dict] = []
    for btn_action in actions:
        if not btn_action.get("is_enabled", True):
            continue
        template = btn_action.get("showroom_action_templates") or btn_action.get("template")
        if not template or not template.get("is_enabled", True):
            continue
        enabled_templates.append(template)

    literal_targets = [resolve_literal_target_sn(t) for t in enabled_templates]
    if enabled_templates and literal_targets and all(literal_targets):
        union_sns = set(literal_targets)
        robots = [r for r in robots if r["sn"] in union_sns]

    selected_sns = {r["sn"] for r in robots}
    robot_by_sn = {r["sn"]: r for r in robots}

    rows_by_sn: dict[str, list[dict]] = defaultdict(list)

    for btn_action in actions:
        if not btn_action.get("is_enabled", True):
            continue
        template = btn_action.get("showroom_action_templates") or btn_action.get("template")
        if not template:
            continue
        if not template.get("is_enabled", True):
            continue

        fixed = resolve_literal_target_sn(template)
        if fixed:
            if fixed not in selected_sns:
                continue
            robot = robot_by_sn.get(fixed)
            if not robot:
                continue
            context = {
                "robot": {"sn": robot["sn"], "nickname": robot.get("nickname") or ""},
                "store": {"pudu_shop_id": store.get("pudu_shop_id", 0), "name": store.get("name", "")},
                "group": {"name": (group or {}).get("name", "")},
            }
            rows_by_sn[robot["sn"]].append(_run_action(template, context))
        else:
            for robot in robots:
                context = {
                    "robot": {"sn": robot["sn"], "nickname": robot.get("nickname") or ""},
                    "store": {"pudu_shop_id": store.get("pudu_shop_id", 0), "name": store.get("name", "")},
                    "group": {"name": (group or {}).get("name", "")},
                }
                rows_by_sn[robot["sn"]].append(_run_action(template, context))

    all_robot_results: list[dict] = []
    ordered_sns: list[str] = []
    for r in robots:
        if r["sn"] in rows_by_sn and r["sn"] not in ordered_sns:
            ordered_sns.append(r["sn"])
    for sn in sorted(rows_by_sn.keys()):
        if sn not in ordered_sns:
            ordered_sns.append(sn)

    for sn in ordered_sns:
        action_results = rows_by_sn[sn]
        robot = robot_by_sn.get(sn) or {}
        all_robot_results.append(
            {
                "robotId": robot.get("id", ""),
                "robotSn": sn,
                "robotNickname": robot.get("nickname"),
                "ok": all(x["ok"] for x in action_results) if action_results else False,
                "actions": action_results,
            }
        )

    finished_at = datetime.datetime.now(datetime.UTC).isoformat()
    overall_ok = all(r["ok"] for r in all_robot_results) if all_robot_results else False

    return {
        "buttonId": button.get("id", ""),
        "buttonName": button.get("name", ""),
        "groupId": button.get("group_id", ""),
        "startedAt": started_at,
        "finishedAt": finished_at,
        "ok": overall_ok,
        "globalActions": [],
        "robots": all_robot_results,
    }


# ─────────────────────────── 狀態輪詢 ───────────────────────────

def extract_map_name_from_robot_payload(obj: object, _depth: int = 0) -> str | None:
    """
    從 get_position / get_by_sn 等回傳結構中盡量取出「當前所在地圖」名稱（與 map 詳情 API 的 map_name 對齊用）。
    """
    if _depth > 10:
        return None
    if isinstance(obj, dict):
        for key in (
            "map_name",
            "mapName",
            "current_map_name",
            "currentMapName",
            "cur_map_name",
            "localization_map_name",
            "loc_map_name",
        ):
            v = obj.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
        for nested_key in ("map_info", "mapInfo", "localization", "map", "position", "cur_map", "data"):
            sub = obj.get(nested_key)
            found = extract_map_name_from_robot_payload(sub, _depth + 1)
            if found:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = extract_map_name_from_robot_payload(item, _depth + 1)
            if found:
                return found
    return None


def _fetch_robot_status(robot: dict, store: dict) -> dict:
    sn = robot["sn"]
    run_state = robot.get("last_run_state")
    position = robot.get("last_position")
    online = False
    current_map_name: str | None = None

    try:
        status_res = call_pudu("GET", "/open-platform-service/v2/status/get_by_sn", query={"sn": sn}, timeout=10)
        data = (status_res.get("json") or {})
        raw = data.get("data") or data
        if isinstance(raw, dict):
            run_state = raw.get("run_state") or raw.get("state") or run_state
            online = bool(raw.get("online", raw.get("is_online", False)))
            current_map_name = extract_map_name_from_robot_payload(raw) or current_map_name
    except Exception:
        pass

    try:
        pos_res = call_pudu("GET", "/open-platform-service/v1/robot/get_position", query={"sn": sn}, timeout=10)
        pos_data = (pos_res.get("json") or {})
        pos_raw = pos_data.get("data") or pos_data
        if isinstance(pos_raw, dict) and ("x" in pos_raw or "position" in pos_raw):
            position = pos_raw
            current_map_name = extract_map_name_from_robot_payload(pos_raw) or current_map_name
    except Exception:
        pass

    return {
        "robotId": robot.get("id", ""),
        "sn": sn,
        "nickname": robot.get("nickname"),
        "runState": run_state,
        "online": online,
        "position": position,
        "currentMapName": current_map_name,
        "updatedAt": datetime.datetime.now(datetime.UTC).isoformat(),
    }


def poll_robot_status(robots: list[dict], store: dict, concurrency: int = 4) -> list[dict]:
    if not robots:
        return []
    results: list[dict] = [{}] * len(robots)
    with ThreadPoolExecutor(max_workers=min(concurrency, len(robots))) as pool:
        fut_map = {pool.submit(_fetch_robot_status, r, store): i for i, r in enumerate(robots)}
        for fut in as_completed(fut_map):
            results[fut_map[fut]] = fut.result()
    return results


# ─────────────────────────── 地圖快照 ───────────────────────────

def fetch_map_detail(shop_id: int | str, map_name: str) -> dict | None:
    """與 API 測試「獲取地圖詳情 V1」相同路徑（/map-service/v1/open/map）。"""
    path = "/map-service/v1/open/map"
    query = {"shop_id": str(shop_id), "map_name": map_name}
    try:
        res = call_pudu("GET", path, query=query, timeout=20)
        if res.get("status_code", 500) >= 400:
            return None
        data = res.get("json") or {}
        return data.get("data") or data
    except Exception:
        return None


def fetch_map_points(sn: str, limit: int = 200) -> list[dict]:
    try:
        res = call_pudu("GET", "/map-service/v1/open/point", query={"sn": sn, "limit": limit, "offset": 0}, timeout=15)
        data = res.get("json") or {}
        raw = data.get("data") or data
        if isinstance(raw, list):
            return raw
        if isinstance(raw, dict):
            for key in ("list", "rows", "items", "points"):
                if isinstance(raw.get(key), list):
                    return raw[key]
    except Exception:
        pass
    return []


def fetch_map_list_by_sn(sn: str, shop_id: int | str | None = None, limit: int = 500) -> list[dict]:
    """用機器人 SN 取得可用地圖清單。"""
    try:
        query = {"sn": sn, "limit": limit, "offset": 0}
        if shop_id is not None and str(shop_id) != "":
            query["shop_id"] = str(shop_id)
        res = call_pudu("GET", "/map-service/v1/open/list", query=query, timeout=15)
        data = res.get("json") or {}
        raw = data.get("data") or data
        if isinstance(raw, dict):
            items = raw.get("list") or raw.get("maps") or raw.get("items") or []
            if isinstance(items, list):
                return items
        if isinstance(raw, list):
            return raw
    except Exception:
        pass
    return []


# ─────────────────────────── Pudu 開放平臺資料 ───────────────────────────

def _paged_fetch(path: str, query: dict | None = None, page_size: int = 100, max_pages: int = 10) -> list[dict]:
    merged: list[dict] = []
    q = dict(query or {})
    for page in range(max_pages):
        q["limit"] = page_size
        q["offset"] = page * page_size
        try:
            res = call_pudu("GET", path, query=q, timeout=15)
            data = res.get("json") or {}
            raw = data.get("data") or data
            items: list[dict] = []
            if isinstance(raw, list):
                items = raw
            elif isinstance(raw, dict):
                for key in ("list", "rows", "items", "data"):
                    if isinstance(raw.get(key), list):
                        items = raw[key]
                        break
            merged.extend(items)
            if len(items) < page_size:
                break
        except Exception:
            break
    return merged


def list_pudu_shops() -> list[dict]:
    items = _paged_fetch("/data-open-platform-service/v1/api/shop")
    shops: dict[int, dict] = {}
    for item in items:
        sid = item.get("shop_id") or item.get("id")
        if not sid:
            continue
        try:
            sid = int(sid)
        except (TypeError, ValueError):
            continue
        shops[sid] = {
            "shop_id": sid,
            "shop_name": item.get("shop_name") or item.get("name") or f"門店 {sid}",
            "company_id": item.get("company_id"),
            "company_name": item.get("company_name"),
        }
    return sorted(shops.values(), key=lambda x: x["shop_id"])


def list_pudu_robots(shop_id: int) -> list[dict]:
    items = _paged_fetch("/data-open-platform-service/v1/api/robot", query={"shop_id": shop_id})
    robots: dict[str, dict] = {}
    for item in items:
        sn = item.get("sn") or item.get("robot_sn") or item.get("pid")
        if not isinstance(sn, str) or not sn:
            continue
        robots[sn] = {
            "sn": sn,
            "shop_id": item.get("shop_id"),
            "shop_name": item.get("shop_name"),
            "product_code": item.get("product_code"),
        }
    return sorted(robots.values(), key=lambda x: x["sn"])


def list_pudu_maps(shop_id: int) -> list[dict]:
    try:
        res = call_pudu("GET", "/data-open-platform-service/v1/api/maps", query={"shop_id": shop_id}, timeout=15)
        data = res.get("json") or {}
        raw = data.get("data") or data
        if isinstance(raw, list):
            return [
                {
                    "map_name": item.get("map_name") or item.get("name") or "",
                    "display_name": item.get("map_alias_name") or item.get("alias_name") or item.get("map_name") or item.get("name") or "",
                }
                for item in raw
                if item.get("map_name") or item.get("name")
            ]
    except Exception:
        pass
    return []
