from __future__ import annotations

import datetime as dt

import streamlit as st

from services.dashboard_common import (
    build_group_robot_options,
    call_api,
    ensure_authenticated,
    extract_payload,
    load_store_context,
    render_kpi,
    render_line_or_bar,
    to_unix,
)


def _status_ok(result: dict) -> bool:
    return 200 <= int(result.get("status_code") or 0) < 300


def _to_dict(payload: object) -> dict:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, list) and payload and isinstance(payload[0], dict):
        return payload[0]
    return {}


def _safe_len_list(payload: object) -> int:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict) and isinstance(payload.get("list"), list):
        return len(payload.get("list") or [])
    return 0


ensure_authenticated("運送機器人儀表板 | Pudu API", "📦")

_store, _robots, groups, robot_map = load_store_context()
robot_options = build_group_robot_options(groups, robot_map, ["運送", "配送", "delivery", "flashbot", "pudubot"])

st.title("📦 運送機器人儀表板")
st.caption("此頁只使用需要 SN 的 API；每台機器各自查詢與彙整。")

if not robot_options:
    st.warning("目前找不到運送群組機器人，請先到設定頁確認群組名稱包含「運送」或「配送」且已綁定機器人。")

with st.form("delivery_sn_dashboard_form"):
    c1, c2 = st.columns([2, 2])
    with c1:
        selected_labels = st.multiselect("運送群組機器人（SN）", options=list(robot_options.keys()))
    with c2:
        default_end = dt.date.today()
        default_start = default_end - dt.timedelta(days=6)
        date_range = st.date_input("日期區間", value=(default_start, default_end))

    c3, c4 = st.columns([1, 1])
    with c3:
        timezone_offset = st.number_input(
            "時區偏移（台灣=8）",
            value=8,
            min_value=-12,
            max_value=14,
            step=1,
            help="填入與 UTC 的時差小時數，例如台灣 +8、日本 +9、UTC 0。",
        )
    with c4:
        limit = st.number_input("日誌筆數限制", min_value=1, max_value=100, value=20, step=1)

    submitted = st.form_submit_button("更新運送儀表板", type="primary", use_container_width=True)

if submitted:
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range

    selected_sns = [
        robot_options[label]
        for label in selected_labels
        if label in robot_options and robot_options[label]
    ]
    if not selected_sns:
        selected_sns = list(robot_options.values())

    time_query = {
        "start_time": to_unix(start_date, end_of_day=False, timezone_offset=int(timezone_offset)),
        "end_time": to_unix(end_date, end_of_day=True, timezone_offset=int(timezone_offset)),
        "timezone_offset": int(timezone_offset),
        "limit": int(limit),
        "offset": 0,
    }

    per_sn_results: dict[str, dict] = {}
    for sn in selected_sns:
        sn_bundle = {
            "狀態V1": call_api("status_by_sn_v1", {"sn": sn}),
            "狀態V2": call_api("status_by_sn_v2", {"sn": sn}),
            "任務狀態": call_api("robot_task_state", {"sn": sn}),
            "呼叫列表": call_api("call_list", {"sn": sn, "limit": int(limit)}),
            "開機日誌": call_api("log_boot", {"sn": sn, **time_query}),
            "充電日誌": call_api("log_charge", {"sn": sn, **time_query}),
            "故障日誌": call_api("log_error", {"sn": sn, **time_query}),
        }
        per_sn_results[sn] = sn_bundle

    st.session_state["_delivery_sn_results"] = per_sn_results

results = st.session_state.get("_delivery_sn_results") or {}
if not results:
    st.info("請先按「更新運送儀表板」。")
    st.stop()

rows = []
for sn, bundle in results.items():
    v1 = _to_dict(extract_payload(bundle.get("狀態V1", {})))
    v2 = _to_dict(extract_payload(bundle.get("狀態V2", {})))
    task_state = _to_dict(extract_payload(bundle.get("任務狀態", {})))

    battery = v1.get("battery") if v1.get("battery") is not None else v2.get("battery")
    is_online = v1.get("is_online") if v1.get("is_online") is not None else v2.get("is_online")

    rows.append(
        {
            "sn": sn,
            "battery": float(battery) if isinstance(battery, (int, float)) else None,
            "is_online": is_online,
            "work_status": v2.get("work_status", v1.get("work_status")),
            "task_status": task_state.get("status", task_state.get("task_status")),
            "call_count": _safe_len_list(extract_payload(bundle.get("呼叫列表", {}))),
            "boot_log_count": _safe_len_list(extract_payload(bundle.get("開機日誌", {}))),
            "charge_log_count": _safe_len_list(extract_payload(bundle.get("充電日誌", {}))),
            "error_log_count": _safe_len_list(extract_payload(bundle.get("故障日誌", {}))),
            "status_ok": _status_ok(bundle.get("狀態V1", {})),
        }
    )

online_count = sum(1 for r in rows if str(r.get("is_online")) == "1")
active_task_count = sum(1 for r in rows if str(r.get("work_status")) not in {"", "-1", "None", "null"})
error_robot_count = sum(1 for r in rows if int(r.get("error_log_count") or 0) > 0)
avg_battery_vals = [float(r.get("battery")) for r in rows if isinstance(r.get("battery"), (int, float))]
avg_battery = round(sum(avg_battery_vals) / len(avg_battery_vals), 1) if avg_battery_vals else None

st.markdown("<div class='section-title'>核心 KPI（SN 維度）</div>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
with k1:
    render_kpi("監控機器數", len(rows))
with k2:
    render_kpi("在線機器數", online_count)
with k3:
    render_kpi("執行中機器數", active_task_count)
with k4:
    render_kpi("平均電量", avg_battery if avg_battery is not None else "-")

c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.markdown("**各機器呼叫數（柱狀圖）**")
        call_rows = [{"label": r["sn"], "call_count": int(r.get("call_count") or 0)} for r in rows]
        render_line_or_bar("呼叫列表筆數", call_rows, max_series=1, height=360)

with c2:
    with st.container(border=True):
        st.markdown("**各機器故障日誌數（柱狀圖）**")
        err_rows = [{"label": r["sn"], "error_count": int(r.get("error_log_count") or 0)} for r in rows]
        render_line_or_bar("故障日誌筆數", err_rows, max_series=1, height=360)
        st.caption(f"有故障日誌機器數：{error_robot_count}")

st.markdown("<div class='section-title' style='margin-top:12px;'>機器狀態明細</div>", unsafe_allow_html=True)
st.dataframe(rows, use_container_width=True)

with st.expander("原始 API 回應（偵錯）"):
    st.json(results)
