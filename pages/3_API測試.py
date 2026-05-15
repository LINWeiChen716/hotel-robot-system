"""
API 測試頁 — 手動簽名發送 Pudu API 請求
"""

import sys
import os
import json
import re
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qsl, quote

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import services.repo as repo
from services.pudu_client import call_pudu
from services.api_definitions import COMMON_APIS


EXAMPLE_START_TIME = "2026/03/01"
EXAMPLE_END_TIME = "2026/03/31"


def _default_param_value(key: str, desc: str | None, *, required: bool):
    field_name = str(key).split(".")[-1].lower()
    if field_name == "start_time":
        return EXAMPLE_START_TIME
    if field_name == "end_time":
        return EXAMPLE_END_TIME
    return f"<必填: {desc}>" if required and desc else ("<必填>" if required else (f"<選填: {desc}>" if desc else "<選填>"))


def _inject_common_value(payload: dict | None, field: str, value):
    if not isinstance(payload, dict) or value in (None, ""):
        return

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if str(k).lower() == field.lower():
                    node[k] = value
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(payload)


def _find_local_group(group_identifier: object) -> tuple[dict | None, list[str]]:
    token = str(group_identifier or "").strip()
    if not token:
        return None, []

    try:
        store = repo.get_or_create_default_store()
        store_id = store.get("id")
        groups = repo.list_groups(store_id) if store_id else []
        robots = repo.list_robots(store_id) if store_id else []
    except Exception:
        return None, []

    token_lower = token.lower()
    target = next(
        (
            g
            for g in groups
            if str(g.get("id") or "").strip() == token
            or str(g.get("name") or "").strip() == token
            or str(g.get("name") or "").strip().lower() == token_lower
        ),
        None,
    )
    if not target:
        return None, []

    sn_by_robot_id = {
        str(r.get("id") or ""): str(r.get("sn") or "").strip()
        for r in robots
        if str(r.get("sn") or "").strip()
    }
    sns = []
    for robot_id in (target.get("robot_ids") or []):
        sn = sn_by_robot_id.get(str(robot_id))
        if sn and sn not in sns:
            sns.append(sn)

    return target, sns


def _response_has_non_empty_data(result: dict | None) -> bool:
    if not isinstance(result, dict):
        return False
    payload = result.get("json")
    if not isinstance(payload, dict):
        return False
    data = payload.get("data")
    if isinstance(data, list):
        return len(data) > 0
    if isinstance(data, dict):
        return len(data) > 0
    return data not in (None, "")


def _status_by_group_local_fallback(api_id: str, group_identifier: object) -> dict | None:
    target_group, sns = _find_local_group(group_identifier)
    if not target_group:
        return None

    if not sns:
        payload = {
            "code": 422,
            "message": "本地群組沒有任何成員，請先到設定 > 群組新增成員。",
            "group": {
                "id": target_group.get("id"),
                "name": target_group.get("name"),
                "member_count": 0,
                "member_sns": [],
            },
            "data": [],
            "errors": [],
        }
        return {
            "status_code": 422,
            "url": f"local://showroom/groups/{target_group.get('id')}",
            "text": json.dumps(payload, ensure_ascii=False),
            "json": payload,
            "sign_str": "",
            "authorization": "",
            "x_date": "",
        }

    if api_id == "status_by_group_id_v1":
        status_path = "/open-platform-service/v1/status/get_by_sn"
    else:
        status_path = "/open-platform-service/v2/status/get_by_sn"

    rows = []
    errors = []
    for sn in sns:
        try:
            one = call_pudu("GET", status_path, query={"sn": sn}, body=None, return_raw=True)
            one_status = int(one.get("status_code") or 0)
            one_json = one.get("json")
            if 200 <= one_status < 300 and isinstance(one_json, dict):
                data = one_json.get("data")
                if isinstance(data, list):
                    rows.extend(data)
                elif data is not None:
                    rows.append(data)
                else:
                    rows.append({"sn": sn})
            else:
                errors.append(
                    {
                        "sn": sn,
                        "status_code": one_status,
                        "message": (one.get("text") or "")[:300],
                    }
                )
        except Exception as exc:
            errors.append({"sn": sn, "status_code": -1, "message": str(exc)})

    payload = {
        "code": 0 if not errors else 207,
        "message": "使用本地群組成員 SN 進行查詢（fallback）",
        "group": {
            "id": target_group.get("id"),
            "name": target_group.get("name"),
            "member_count": len(sns),
            "member_sns": sns,
        },
        "data": rows,
        "errors": errors,
    }
    return {
        "status_code": 200 if not errors else 207,
        "url": f"local://showroom/groups/{target_group.get('id')}",
        "text": json.dumps(payload, ensure_ascii=False),
        "json": payload,
        "sign_str": "",
        "authorization": "",
        "x_date": "",
    }


def _merge_robot_group_list_with_local(cloud_result: dict | None) -> dict:
    try:
        store = repo.get_or_create_default_store()
        store_id = store.get("id")
        local_groups = repo.list_groups(store_id) if store_id else []
    except Exception:
        local_groups = []

    local_groups = [
        g for g in local_groups
        if not str(g.get("name") or "").strip().startswith("_")
    ]

    cloud_json = (cloud_result or {}).get("json")
    cloud_data = []
    if isinstance(cloud_json, dict):
        data = cloud_json.get("data")
        if isinstance(data, list):
            cloud_data = data

    existed_keys = set()
    for row in cloud_data:
        if not isinstance(row, dict):
            continue
        for k in ("group_id", "id", "name", "group_name"):
            v = str(row.get(k) or "").strip()
            if v:
                existed_keys.add(v)

    local_rows = []
    for g in local_groups:
        gid = str(g.get("id") or "").strip()
        gname = str(g.get("name") or "").strip()
        if not gid or not gname:
            continue
        if gid in existed_keys or gname in existed_keys:
            continue
        local_rows.append(
            {
                "group_id": gid,
                "id": gid,
                "name": gname,
                "group_name": gname,
                "member_count": len(g.get("robot_ids") or []),
                "source": "local_showroom",
            }
        )

    merged = list(cloud_data) + local_rows
    payload = cloud_json if isinstance(cloud_json, dict) else {"code": 0, "message": "ok"}
    payload["data"] = merged
    payload["local_group_count"] = len(local_rows)

    return {
        "status_code": int((cloud_result or {}).get("status_code") or 200),
        "url": str((cloud_result or {}).get("url") or "local://showroom/robot/group/list"),
        "text": json.dumps(payload, ensure_ascii=False),
        "json": payload,
        "sign_str": str((cloud_result or {}).get("sign_str") or ""),
        "authorization": str((cloud_result or {}).get("authorization") or ""),
        "x_date": str((cloud_result or {}).get("x_date") or ""),
    }


def _robot_list_by_local_group(group_identifier: object) -> dict | None:
    target_group, sns = _find_local_group(group_identifier)
    if not target_group:
        return None

    try:
        store = repo.get_or_create_default_store()
        store_id = store.get("id")
        robots = repo.list_robots(store_id) if store_id else []
    except Exception:
        robots = []

    robot_by_sn = {
        str(r.get("sn") or "").strip(): r
        for r in robots
        if str(r.get("sn") or "").strip()
    }

    rows = []
    for sn in sns:
        r = robot_by_sn.get(sn, {})
        rows.append(
            {
                "sn": sn,
                "nickname": r.get("nickname"),
                "is_enabled": bool(r.get("is_enabled")) if r else True,
                "group_id": target_group.get("id"),
                "group_name": target_group.get("name"),
                "source": "local_showroom",
            }
        )

    payload = {
        "code": 0,
        "message": "使用本地群組成員查詢結果",
        "group": {
            "id": target_group.get("id"),
            "name": target_group.get("name"),
            "member_count": len(rows),
        },
        "data": rows,
    }
    return {
        "status_code": 200,
        "url": f"local://showroom/groups/{target_group.get('id')}/robots",
        "text": json.dumps(payload, ensure_ascii=False),
        "json": payload,
        "sign_str": "",
        "authorization": "",
        "x_date": "",
    }


@st.cache_data(ttl=30)
def _load_common_values():
    try:
        store = repo.get_or_create_default_store()
        store_id = store.get("id")
        shop_id = str(store.get("pudu_shop_id") or "").strip()
        robots = repo.list_robots(store_id) if store_id else []
        map_tabs = repo.list_map_tabs(store_id) if store_id else []
        groups = repo.list_groups(store_id) if store_id else []
    except Exception:
        return "", [], [], []

    sns = []
    for r in robots:
        sn = str(r.get("sn") or "").strip()
        if sn and sn not in sns:
            sns.append(sn)

    maps = []
    for m in map_tabs:
        name = str(m.get("map_name") or "").strip()
        if name and name not in maps:
            maps.append(name)

    group_rows = []
    for g in groups:
        gname = str(g.get("name") or "").strip()
        gid = str(g.get("id") or "").strip()
        if gname.startswith("_"):
            continue
        if gname and gid:
            group_rows.append(
                {
                    "id": gid,
                    "name": gname,
                    "robot_ids": g.get("robot_ids") or [],
                }
            )

    return shop_id, sns, maps, group_rows


def _build_callback_url() -> tuple[str, bool]:
    public_url = str(os.getenv("PUDU_CALLBACK_PUBLIC_URL") or "").strip()
    if public_url:
        return public_url, False

    host = str(os.getenv("PUDU_CALLBACK_HOST") or "0.0.0.0").strip() or "0.0.0.0"
    port = str(os.getenv("PUDU_CALLBACK_PORT") or "8787").strip() or "8787"
    path = str(os.getenv("PUDU_CALLBACK_PATH") or "/pudu/callback").strip() or "/pudu/callback"
    if not path.startswith("/"):
        path = f"/{path}"

    # host=0.0.0.0 僅代表監聽，非外部可連線地址。
    need_hint = host in {"0.0.0.0", "127.0.0.1", "localhost"}
    return f"http://{host}:{port}{path}", need_hint


def _diagnose_voice_list_failure(sn: object) -> dict:
    sn_text = str(sn or "").strip()
    if not sn_text:
        return {"sn": "", "status_ok": False, "message": "未提供 sn，無法進一步診斷。"}

    try:
        res = call_pudu(
            "GET",
            "/open-platform-service/v1/status/get_by_sn",
            query={"sn": sn_text},
            body=None,
            return_raw=True,
        )
    except Exception as exc:
        return {
            "sn": sn_text,
            "status_ok": False,
            "message": f"語音列表失敗後，連機器狀態也查不到：{exc}",
        }

    payload = res.get("json") or {}
    data = payload.get("data") or payload
    online = None
    if isinstance(data, dict):
        online = data.get("is_online")
        if online is None:
            online = data.get("online")

    try:
        online_int = int(online) if online is not None else None
    except (TypeError, ValueError):
        online_int = None

    if online_int == 1:
        message = "機器目前顯示在線，但語音列表仍逾時。通常是雲端到機器的連線不穩，建議稍後重試，並確認機器目前可正常被控制。"
    elif online_int == 0:
        message = "機器目前顯示已關機或不可用，因此語音列表會失敗。"
    elif online_int == -1:
        message = "機器目前顯示離線，雲端無法連到機器，因此語音列表會失敗。"
    else:
        message = "已查詢機器狀態，但無法判斷在線欄位；請確認此 SN 是否為 Kettybot，且機器已連上網路。"

    return {
        "sn": sn_text,
        "status_ok": 200 <= int(res.get("status_code") or 0) < 300,
        "http_status": res.get("status_code"),
        "online": online_int,
        "status_data": data if isinstance(data, dict) else payload,
        "message": message,
    }


def _build_param_template(api_config: dict, method: str, selected_type: str | None = None) -> dict:
    template: dict = {}
    required = dict(api_config.get("required_params", {}))
    optional = dict(api_config.get("optional_params", {}))
    dyn_required, dyn_optional = _resolve_dynamic_param_spec(api_config, selected_type)
    required.update(dyn_required)
    optional.update(dyn_optional)

    for key, desc in required.items():
        _set_nested_value(template, key, _default_param_value(key, desc, required=True))
    for key, desc in optional.items():
        if _get_nested_value(template, key) is None:
            _set_nested_value(template, key, _default_param_value(key, desc, required=False))
    return template


def _build_param_rows(api_config: dict, selected_type: str | None = None) -> list[dict]:
    rows = []
    required = dict(api_config.get("required_params", {}))
    optional = dict(api_config.get("optional_params", {}))
    dyn_required, dyn_optional = _resolve_dynamic_param_spec(api_config, selected_type)
    required.update(dyn_required)
    optional.update(dyn_optional)

    for key, desc in required.items():
        rows.append({
            "參數": key,
            "必填": "是",
            "說明": desc or "",
        })
    for key, desc in optional.items():
        if key not in required:
            rows.append({
                "參數": key,
                "必填": "否",
                "說明": desc or "",
            })
    return rows


def _format_supported_robots(api_config: dict) -> str:
    robots = api_config.get("supported_robots", [])
    if isinstance(robots, list) and robots:
        return "、".join(str(item) for item in robots)
    return "待補充"


def _parse_example_query(example_value):
    if isinstance(example_value, dict):
        return example_value
    if isinstance(example_value, str):
        query = example_value.lstrip("?")
        return {k: v for k, v in parse_qsl(query, keep_blank_values=True)}
    return {}


def _parse_example_body(example_value):
    if isinstance(example_value, dict):
        return example_value
    if isinstance(example_value, str):
        try:
            parsed = json.loads(example_value)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            return {}
    return {}


def _loads_relaxed_json(raw_text: str):
    text = (raw_text or "").strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError as first_err:
        # Tolerate trailing commas before } or ] in user input.
        cleaned = re.sub(r",\s*([}\]])", r"\1", text)
        if cleaned != text:
            try:
                parsed = json.loads(cleaned)
                return parsed
            except json.JSONDecodeError:
                pass
        raise first_err


def _get_timezone_offset_hours(query: dict | None, body: dict | None) -> int:
    raw = None
    if isinstance(query, dict):
        raw = query.get("timezone_offset")
    if raw is None and isinstance(body, dict):
        raw = body.get("timezone_offset")
    try:
        tz = int(raw) if raw is not None else 0
    except (TypeError, ValueError):
        tz = 0
    return max(-12, min(14, tz))


def _to_unix_ts(value, *, end_of_day: bool, tz_offset_hours: int) -> int | None:
    if value is None:
        return None

    # Already integer-like value.
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())

    if not isinstance(value, str):
        return None

    s = value.strip()
    if not s:
        return None

    tzinfo = timezone(timedelta(hours=tz_offset_hours))

    # YYYY-MM-DD or YYYY/MM/DD
    m = re.fullmatch(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", s)
    if m:
        y, mo, d = map(int, m.groups())
        if end_of_day:
            dt = datetime(y, mo, d, 23, 59, 59, tzinfo=tzinfo)
        else:
            dt = datetime(y, mo, d, 0, 0, 0, tzinfo=tzinfo)
        return int(dt.timestamp())

    # YYYY-MM-DD HH:MM[:SS] or YYYY/MM/DD HH:MM[:SS]
    m_dt = re.fullmatch(
        r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})[ T](\d{1,2}):(\d{1,2})(?::(\d{1,2}))?",
        s,
    )
    if m_dt:
        y, mo, d, hh, mm, ss = m_dt.groups()
        sec = int(ss) if ss is not None else 0
        dt = datetime(int(y), int(mo), int(d), int(hh), int(mm), sec, tzinfo=tzinfo)
        return int(dt.timestamp())

    # ISO datetime (fallback)
    s2 = s.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s2)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tzinfo)
        return int(dt.timestamp())
    except ValueError:
        return None


def _convert_time_fields_inplace(payload: dict | None, *, tz_offset_hours: int) -> None:
    if not isinstance(payload, dict):
        return

    def walk(node):
        if isinstance(node, dict):
            for k, v in list(node.items()):
                lk = str(k).lower()
                if lk == "start_time":
                    ts = _to_unix_ts(v, end_of_day=False, tz_offset_hours=tz_offset_hours)
                    if ts is not None:
                        node[k] = ts
                elif lk == "end_time":
                    ts = _to_unix_ts(v, end_of_day=True, tz_offset_hours=tz_offset_hours)
                    if ts is not None:
                        node[k] = ts
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(payload)


def _set_nested_value(obj: dict, dotted_key: str, value):
    parts = dotted_key.split(".")
    cursor = obj
    for part in parts[:-1]:
        child = cursor.get(part)
        if not isinstance(child, dict):
            child = {}
            cursor[part] = child
        cursor = child
    cursor[parts[-1]] = value


def _get_nested_value(obj: dict, dotted_key: str):
    parts = dotted_key.split(".")
    cursor = obj
    for part in parts[:-1]:
        cursor = cursor.get(part)
        if not isinstance(cursor, dict):
            return None
    return cursor.get(parts[-1]) if isinstance(cursor, dict) else None


def _deep_merge_dict(base: dict, patch: dict) -> dict:
    merged = dict(base)
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(merged.get(k), dict):
            merged[k] = _deep_merge_dict(merged[k], v)
        else:
            merged[k] = v
    return merged


def _resolve_dynamic_param_spec(api_config: dict, selected_type: str | None) -> tuple[dict, dict]:
    required = {}
    optional = {}
    rules = api_config.get("type_param_rules") or {}
    by_type = rules.get("by_type") if isinstance(rules, dict) else {}
    if not isinstance(by_type, dict) or selected_type is None:
        return required, optional
    selected_rule = by_type.get(str(selected_type))
    if isinstance(selected_rule, dict):
        if isinstance(selected_rule.get("required_params"), dict):
            required.update(selected_rule["required_params"])
        if isinstance(selected_rule.get("optional_params"), dict):
            optional.update(selected_rule["optional_params"])
    return required, optional


def _resolve_dynamic_example_body(api_config: dict, selected_type: str | None) -> dict:
    rules = api_config.get("type_param_rules") or {}
    by_type = rules.get("by_type") if isinstance(rules, dict) else {}
    if not isinstance(by_type, dict) or selected_type is None:
        return {}
    selected_rule = by_type.get(str(selected_type))
    if isinstance(selected_rule, dict) and isinstance(selected_rule.get("example_body"), dict):
        return dict(selected_rule["example_body"])
    return {}


def _get_type_options(api_config: dict) -> list[tuple[str, str]]:
    options = api_config.get("type_options")
    if not isinstance(options, dict):
        return []

    def sort_key(item: tuple[str, str]):
        key = item[0]
        try:
            return (0, int(key))
        except ValueError:
            return (1, key)

    return sorted([(str(k), str(v)) for k, v in options.items()], key=sort_key)


st.set_page_config(page_title="API 測試 — Pudu 控制台", page_icon="🔧", layout="wide")

if not st.session_state.get("authenticated"):
    st.warning("請先從首頁登入。")
    st.stop()

st.title("🔧 API 測試")
st.caption("自動套用 HMAC-SHA1 簽名，路徑毋需填 /pudu-entry/ 前綴。")

# ─────────────── 快速搜尋 ─────────────────────────────────────────
with st.expander("🔍 快速搜尋 API（名稱／路徑／ID）", expanded=False):
    search_kw = st.text_input("輸入關鍵字搜尋", placeholder="例如：清潔、recharge、/map-service", key="api_search_kw")
    if search_kw.strip():
        kw = search_kw.strip().lower()
        matched = []
        for cat, apis in COMMON_APIS.items():
            for api in apis:
                if (kw in api.get("name", "").lower()
                        or kw in api.get("path", "").lower()
                        or kw in api.get("id", "").lower()
                        or kw in api.get("description", "").lower()):
                    matched.append((cat, api))
        if matched:
            options = [f"[{cat}] {api['name']}  —  {api['path']}" for cat, api in matched]
            chosen = st.selectbox("搜尋結果", options, key="api_search_result")
            idx = options.index(chosen)
            chosen_cat, chosen_api = matched[idx]
            st.info(f"📌 **Method**: {chosen_api['method']} | **Path**: {chosen_api['path']}")
            if st.button("⬇ 套用到下方送出區", key="apply_search"):
                st.session_state["_search_applied"] = chosen_api
        else:
            st.warning("找不到符合的 API，請換關鍵字。")

# 從搜尋套用
_applied = st.session_state.pop("_search_applied", None)
selected_task_type = None
selected_action = None

# ─────────────── 輸入 ────────────────────────────────────────────
api_group = st.selectbox("常用 API", ["自訂輸入"] + list(COMMON_APIS.keys()), key="api_group_select")
method = "GET"
if not _applied and api_group == "自訂輸入":
    method = st.selectbox("Method", ["GET", "POST"], key="method_select")

# 若有從搜尋套用的 API，直接顯示並進入送出區
if _applied:
    api_config = _applied
    path = _applied["path"]
    method = _applied.get("method", "GET")
    selected_name = _applied["name"]
    st.markdown("---")
    st.subheader(f"📖 {selected_name}")
    st.markdown(f"**說明**\n\n{api_config.get('description', '')}")
    st.markdown(f"**可使用機器**\n\n{_format_supported_robots(api_config)}")
    type_options = _get_type_options(api_config)
    if type_options:
        type_label = api_config.get("type_label", "任務類型")
        option_keys = [k for k, _ in type_options]
        option_map = {k: v for k, v in type_options}
        body_example = _parse_example_body((api_config.get("examples") or {}).get("body"))
        type_field = api_config.get("type_field_name", "type")
        default_type_val = _get_nested_value(body_example, type_field) if body_example else None
        default_type = str(default_type_val) if default_type_val is not None else option_keys[0]
        default_idx = option_keys.index(default_type) if default_type in option_keys else 0
        selected_task_type = st.selectbox(
            type_label,
            option_keys,
            index=default_idx,
            format_func=lambda k: f"{k} - {option_map.get(k, '')}",
            key=f"type_sel_{api_config.get('id', 'x')}_search",
        )
        if api_config.get("type_hint"):
            st.caption(api_config["type_hint"])
    action_opts = api_config.get("action_options")
    if action_opts and isinstance(action_opts, dict):
        action_label = api_config.get("action_label", "動作選項 (action)")
        ak = sorted(action_opts.keys())
        selected_action = st.selectbox(
            action_label,
            ak,
            format_func=lambda k: f"{k} — {action_opts.get(k, '')}",
            key=f"action_sel_{api_config.get('id', 'x')}_search",
        )

    st.markdown("**參數總覽（必填已標示）**")
    param_rows = _build_param_rows(api_config, selected_task_type)
    if param_rows:
        st.dataframe(param_rows, use_container_width=True, hide_index=True)
    else:
        st.markdown("無")
    st.markdown(f"**回應說明**\n\n{api_config.get('response_description', '')}")
    st.markdown("---")
    st.info(f"📌 **Path**: {path} | **Method**: {method}")

# 根據選擇 populate path 和 method
if not _applied:
    path = None
    api_config = None
if not _applied and api_group != "自訂輸入":
    api_list = COMMON_APIS[api_group]
    api_names = [api["name"] for api in api_list if isinstance(api, dict) and api.get("name")]

    if not api_names:
        st.warning(f"『{api_group}』目前沒有可選 API。")
        api_config = None
        path = None
    else:
        selected_name = st.selectbox("選擇 API", api_names, key="api_name_select")
        api_config = next((api for api in api_list if isinstance(api, dict) and api.get("name") == selected_name), None)
        if not isinstance(api_config, dict):
            st.error("找不到對應 API 設定，請重新選擇分組或 API。")
            path = None
        else:
            path = api_config.get("path")
            method = api_config.get("method", "GET")

    if not isinstance(api_config, dict):
        st.stop()
    
    # 詳細說明區塊
    st.markdown("---")
    st.subheader(f"📖 {selected_name}")
    
    # 描述
    st.markdown(f"**說明**\n\n{api_config.get('description', '')}")
    st.markdown(f"**可使用機器**\n\n{_format_supported_robots(api_config)}")
    type_options = _get_type_options(api_config)
    if type_options:
        type_label = api_config.get("type_label", "任務類型")
        option_keys = [k for k, _ in type_options]
        option_map = {k: v for k, v in type_options}
        body_example = _parse_example_body((api_config.get("examples") or {}).get("body"))
        type_field = api_config.get("type_field_name", "type")
        default_type_val = _get_nested_value(body_example, type_field) if body_example else None
        default_type = str(default_type_val) if default_type_val is not None else option_keys[0]
        default_idx = option_keys.index(default_type) if default_type in option_keys else 0
        selected_task_type = st.selectbox(
            type_label,
            option_keys,
            index=default_idx,
            format_func=lambda k: f"{k} - {option_map.get(k, '')}",
            key=f"type_sel_{api_config.get('id', 'x')}_group",
        )
        if api_config.get("type_hint"):
            st.caption(api_config["type_hint"])
    action_opts = api_config.get("action_options")
    if action_opts and isinstance(action_opts, dict):
        action_label = api_config.get("action_label", "動作選項 (action)")
        ak = sorted(action_opts.keys())
        selected_action = st.selectbox(
            action_label,
            ak,
            format_func=lambda k: f"{k} — {action_opts.get(k, '')}",
            key=f"action_sel_{api_config.get('id', 'x')}_group",
        )
    
    # 參數總覽（所有參數 + 必填標示）
    st.markdown("**參數總覽（必填已標示）**")
    param_rows = _build_param_rows(api_config, selected_task_type)
    if param_rows:
        st.dataframe(param_rows, use_container_width=True, hide_index=True)
    else:
        st.markdown("無")
    
    # 回應說明
    st.markdown(f"**回應說明**\n\n{api_config.get('response_description', '')}")

    # 回調地址提示（notifySwitchMap / notifyRobotMoveState / notifyRobotPose）
    callback_example = api_config.get("callback_example")
    callback_url, callback_need_hint = _build_callback_url()
    callback_types_for_hint = {"notifySwitchMap", "notifyRobotMoveState", "notifyRobotPose"}
    callback_type = str(callback_example.get("callback_type") or "") if isinstance(callback_example, dict) else ""
    should_show_callback_hint = (
        isinstance(api_config, dict)
        and (
            str(api_config.get("id") or "") in {"switch_map", "position_command"}
            or callback_type in callback_types_for_hint
        )
    )

    if should_show_callback_hint:
        st.markdown("**📡 回調地址（Callback URL）**")
        st.caption("notifySwitchMap / notifyRobotMoveState / notifyRobotPose 都需要填入同一個回調地址")
        st.code(callback_url, language="text")
        if callback_need_hint:
            st.info("目前顯示的是本機監聽位址，請改成平台可連線的公開網址（可設 PUDU_CALLBACK_PUBLIC_URL）。")

    if (
        isinstance(api_config, dict)
        and callback_type in callback_types_for_hint
        and isinstance(callback_example, dict)
        and callback_example
    ):
        st.markdown("**📣 回調通知範例（Callback）**")
        if callback_type:
            st.caption(f"callback_type: `{callback_type}`")
        st.json(callback_example)
    
    # 範例
    examples = api_config.get("examples", {})
    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        if "query" in examples:
            st.markdown("**📋 查詢參數範例**")
            st.json(_parse_example_query(examples.get("query")))
    with col_ex2:
        if "body" in examples:
            st.markdown("**📋 Body 範例**")
            type_body_example = _resolve_dynamic_example_body(api_config, selected_task_type)
            body_example = type_body_example or _parse_example_body(examples.get("body"))
            st.json(body_example)
    
    st.markdown("---")
    st.info(f"📌 **Path**: {path} | **Method**: {method}")
elif not _applied:
    path = st.text_input("Path", value="/map-service/v1/open/map", placeholder="/xxx-service/v1/open/yyy")

col_q, col_b = st.columns(2)
with col_q:
    default_query_obj = {}
    if api_config:
        examples = api_config.get("examples", {})
        if method == "GET":
            default_query_obj = _build_param_template(api_config, method, selected_task_type)
            default_query_obj = _deep_merge_dict(default_query_obj, _parse_example_query(examples.get("query")))
        else:
            default_query_obj = _parse_example_query(examples.get("query"))

    quick_shop_id, quick_sns, quick_maps, quick_groups = _load_common_values()
    with st.expander("⚡ 快速帶入：門店ID / 機器SN / 地圖名稱", expanded=False):
        st.markdown(f"門店ID：**{quick_shop_id or '未設定'}**")
        if quick_sns:
            st.markdown("機器人 SN（全部）")
            st.code("\n".join(quick_sns), language="text")
        else:
            st.caption("尚無可用機器人 SN")
        if quick_maps:
            st.markdown("地圖名稱")
            st.code("\n".join(quick_maps), language="text")
        else:
            st.caption("尚無地圖名稱")

        if quick_groups:
            st.markdown("可用本地群組（可帶入 group_id）")
            st.dataframe(
                [
                    {
                        "群組名稱": g["name"],
                        "group_id": g["id"],
                        "群組台數": len(g.get("robot_ids") or []),
                    }
                    for g in quick_groups
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.caption("尚無本地群組")

        c1, c2, c3, c4 = st.columns(4)
        chosen_sn = c1.selectbox("帶入 SN", [""] + quick_sns, index=0, key="quick_sn_select")
        chosen_map = c2.selectbox("帶入 map_name", [""] + quick_maps, index=0, key="quick_map_select")
        use_shop = c3.checkbox("帶入 shop_id", value=True, key="quick_use_shop")
        group_labels = [f"{g['name']} ({g['id']})" for g in quick_groups]
        chosen_group_label = c4.selectbox("帶入 group_id", [""] + group_labels, index=0, key="quick_group_select")
        if st.button("套用到 Query / Body", key="quick_apply_common_values", use_container_width=True):
            if use_shop and quick_shop_id:
                _inject_common_value(default_query_obj, "shop_id", quick_shop_id)
            if chosen_sn:
                _inject_common_value(default_query_obj, "sn", chosen_sn)
                _inject_common_value(default_query_obj, "pid", chosen_sn)
            if chosen_map:
                _inject_common_value(default_query_obj, "map_name", chosen_map)
            if chosen_group_label:
                gid = chosen_group_label.rsplit("(", 1)[-1].rstrip(")").strip()
                if gid:
                    _inject_common_value(default_query_obj, "group_id", gid)

    default_query = json.dumps(default_query_obj, ensure_ascii=False, indent=2)
    query_raw = st.text_area("Query Params（JSON）", value=default_query, height=150)
with col_b:
    default_body_obj = {}
    if api_config:
        examples = api_config.get("examples", {})
        default_body_obj = _build_param_template(api_config, method, selected_task_type)
        type_body_example = _resolve_dynamic_example_body(api_config, selected_task_type)
        base_body_example = type_body_example or _parse_example_body(examples.get("body"))
        default_body_obj = _deep_merge_dict(default_body_obj, base_body_example)
        if selected_task_type is not None and api_config.get("type_options"):
            field_name = api_config.get("type_field_name", "type")
            try:
                val = int(selected_task_type)
            except (ValueError, TypeError):
                val = selected_task_type
            _set_nested_value(default_body_obj, field_name, val)
        if selected_action is not None and api_config.get("action_options"):
            field_name = api_config.get("action_field_name", "action")
            _set_nested_value(default_body_obj, field_name, selected_action)
        if method == "GET":
            default_body_obj = {}

    # 與 Query 相同，若有快速帶入值，Body 也同步覆蓋常用欄位。
    if api_config:
        quick_shop_id, quick_sns, quick_maps, _quick_groups = _load_common_values()
        chosen_sn = st.session_state.get("quick_sn_select", "")
        chosen_map = st.session_state.get("quick_map_select", "")
        use_shop = st.session_state.get("quick_use_shop", True)
        chosen_group_label = st.session_state.get("quick_group_select", "")
        if use_shop and quick_shop_id:
            _inject_common_value(default_body_obj, "shop_id", quick_shop_id)
        if chosen_sn:
            _inject_common_value(default_body_obj, "sn", chosen_sn)
            _inject_common_value(default_body_obj, "pid", chosen_sn)
        if chosen_map:
            _inject_common_value(default_body_obj, "map_name", chosen_map)
        if chosen_group_label:
            gid = chosen_group_label.rsplit("(", 1)[-1].rstrip(")").strip()
            if gid:
                _inject_common_value(default_body_obj, "group_id", gid)

    default_body = json.dumps(default_body_obj, ensure_ascii=False, indent=2)
    body_raw = st.text_area("Request Body（JSON）", value=default_body, height=150, disabled=(method == "GET"))

submit = st.button("🚀 送出請求", type="primary")
st.caption("提示：start_time / end_time 可填 YYYY/MM/DD、YYYY-MM-DD、YYYY/MM/DD HH:MM[:SS]、YYYY-MM-DD HH:MM[:SS]，系統會依 timezone_offset 自動轉成 integer 秒級時間戳。")

# ─────────────── 執行 ────────────────────────────────────────────
if submit:
    if not path.strip():
        st.error("請填入 Path。")
        st.stop()

    # 解析 JSON
    try:
        query = _loads_relaxed_json(query_raw)
    except json.JSONDecodeError as e:
        st.error(f"Query Params JSON 解析失敗：{e}")
        st.stop()

    try:
        body = _loads_relaxed_json(body_raw) if method != "GET" else None
    except json.JSONDecodeError as e:
        st.error(f"Body JSON 解析失敗：{e}")
        st.stop()

    tz_offset_hours = _get_timezone_offset_hours(query, body)
    _convert_time_fields_inplace(query, tz_offset_hours=tz_offset_hours)
    _convert_time_fields_inplace(body, tz_offset_hours=tz_offset_hours)

    with st.spinner("發送中…"):
        try:
            request_path = path.strip()
            request_query = query or None
            local_compat_message = None

            # 依你的 API 地圖測試.py 邏輯：僅「獲取地圖詳情 V1」走模板替換
            # Url = "...?shop_id=${shop_id}&map_name=${map_name}"
            # Url = Url.replace("${map_name}", quote(map_name))
            # Url = Url.replace("${shop_id}", quote(shop_id))
            if isinstance(api_config, dict) and api_config.get("id") == "map_detail_v1":
                shop_id_val = (query or {}).get("shop_id")
                map_name_val = (query or {}).get("map_name")
                if shop_id_val in (None, "") or map_name_val in (None, ""):
                    st.error("獲取地圖詳情 V1 需要在 Query Params 填入 shop_id 與 map_name。")
                    st.stop()
                request_path = (
                    "/map-service/v1/open/map?shop_id=${shop_id}&map_name=${map_name}"
                    .replace("${map_name}", quote(str(map_name_val), safe=""))
                    .replace("${shop_id}", quote(str(shop_id_val), safe=""))
                )
                request_query = None

            api_id = str(api_config.get("id") or "") if isinstance(api_config, dict) else ""

            used_local_group_fallback = False
            if api_id == "robot_group_list":
                cloud_result = None
                try:
                    cloud_result = call_pudu(method, request_path, query=request_query, body=body, return_raw=True)
                except Exception:
                    cloud_result = None
                result = _merge_robot_group_list_with_local(cloud_result)
                local_compat_message = "已合併顯示本地群組：data 中 source=local_showroom 的項目為本地群組。"

            elif api_id == "robot_list_by_device_and_group":
                group_id_val = None
                if isinstance(query, dict):
                    group_id_val = query.get("group_id")
                if group_id_val in (None, "") and isinstance(body, dict):
                    group_id_val = body.get("group_id")

                local_group_result = _robot_list_by_local_group(group_id_val)
                if local_group_result is not None:
                    result = local_group_result
                    local_compat_message = "已用本地群組查詢機器清單：這是本地資料，不是 Pudu 雲端官方群組資料。"
                else:
                    result = call_pudu(method, request_path, query=request_query, body=body, return_raw=True)

            elif api_id in {"status_by_group_id_v1", "status_by_group_id_v2"}:
                group_id_val = None
                if isinstance(query, dict):
                    group_id_val = query.get("group_id")
                if group_id_val in (None, "") and isinstance(body, dict):
                    group_id_val = body.get("group_id")

                cloud_result = None
                cloud_error = None
                try:
                    cloud_result = call_pudu(method, request_path, query=request_query, body=body, return_raw=True)
                except Exception as exc:
                    cloud_error = exc

                local_group_result = _status_by_group_local_fallback(api_id, group_id_val)
                if local_group_result is not None and not _response_has_non_empty_data(cloud_result):
                    result = local_group_result
                    used_local_group_fallback = True
                    local_compat_message = "已改用本地群組成員 SN 查詢（fallback）。"
                else:
                    if cloud_result is not None:
                        result = cloud_result
                    elif local_group_result is not None:
                        result = local_group_result
                        used_local_group_fallback = True
                        local_compat_message = "官方查詢失敗，已改用本地群組成員 SN 查詢。"
                    else:
                        raise cloud_error or RuntimeError("群組狀態查詢失敗")
            else:
                result = call_pudu(method, request_path, query=request_query, body=body, return_raw=True)
        except Exception as exc:
            st.error(f"請求失敗：{exc}")
            st.stop()

    if local_compat_message:
        st.info(local_compat_message)

    if used_local_group_fallback:
        g = ((result or {}).get("json") or {}).get("group") or {}
        gname = g.get("name") or "(未命名群組)"
        mcount = int(g.get("member_count") or 0)
        msns = g.get("member_sns") or []
        st.info(
            f"已改用本地群組查詢：{gname}（{mcount} 台）。"
            f"成員 SN：{', '.join(msns) if msns else '無'}"
        )

    # ─ 顯示結果 ──────────────────────────────────────────────────
    st.markdown("---")
    col_info, col_status = st.columns([4, 1])
    with col_info:
        st.markdown(f"**完整 URL**：`{result.get('url', '?')}`")
    with col_status:
        status_code = result.get("status_code", 0)
        color = "green" if 200 <= status_code < 300 else "red"
        st.markdown(f"**HTTP {status_code}**")

    if isinstance(api_config, dict) and str(api_config.get("id") or "") == "voice_list":
        query_sn = query.get("sn") if isinstance(query, dict) else None
        body_sn = body.get("sn") if isinstance(body, dict) else None
        voice_sn = query_sn or body_sn
        result_text = str(result.get("text") or "")
        if not (200 <= int(status_code or 0) < 300):
            st.warning("獲取語音列表僅支援 Kettybot。若機器離線、關機，或雲端暫時連不到機器，常會回 CLOUD_OPEN_TIMEOUT。")
            diagnosis = _diagnose_voice_list_failure(voice_sn)
            st.info(diagnosis.get("message") or "")
            with st.expander("獲取語音列表診斷資訊"):
                st.json(diagnosis)
        elif "CLOUD_OPEN_TIMEOUT" in result_text:
            st.warning("回應包含 CLOUD_OPEN_TIMEOUT，代表雲端與機器通訊逾時；可展開下方診斷資訊確認機器在線狀態。")
            diagnosis = _diagnose_voice_list_failure(voice_sn)
            with st.expander("獲取語音列表診斷資訊"):
                st.json(diagnosis)

    tab_json, tab_raw = st.tabs(["JSON", "Raw"])
    resp_json = result.get("json")
    with tab_json:
        if resp_json is not None:
            st.json(resp_json)
        else:
            st.warning("回應非 JSON 格式，請查看 Raw 頁籤。")
    with tab_raw:
        st.code(result.get("text", ""), language="text")

    # 顯示簽名資訊（方便 debug）
    with st.expander("🔑 簽名 Debug 資訊"):
        st.json({k: v for k, v in result.items() if k in ("sign_str", "authorization", "x_date")})
