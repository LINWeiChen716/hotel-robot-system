from __future__ import annotations

import datetime as dt

import streamlit as st

from services.dashboard_common import (
    call_api,
    collect_numeric_items,
    ensure_authenticated,
    extract_payload,
    find_chart_blocks,
    load_store_context,
    render_kpi,
    render_line_or_bar,
    to_unix,
)


def _render_status(result: dict) -> None:
    status = int(result.get("status_code") or 0)
    st.caption(f"HTTP {status}")
    if not (200 <= status < 300):
        st.error((result.get("text") or "")[:260] or "查詢失敗")


ensure_authenticated("門店儀表板 | Pudu API", "🏬")

store, robots, _groups, _robot_map = load_store_context()
shop_id = str(store.get("pudu_shop_id") or "").strip()

st.title("🏬 門店儀表板")
st.caption("此頁只使用 shop_id 維度 API：門店摘要、門店趨勢、跨門店排行與門店清單。")

with st.form("shop_dashboard_form"):
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        mode = st.selectbox("門店模式", ["目前門店", "跨門店"], index=0)
        st.text_input("目前設定門店 ID", value=shop_id or "未設定", disabled=True)
    with c2:
        default_end = dt.date.today()
        default_start = default_end - dt.timedelta(days=6)
        date_range = st.date_input("日期區間", value=(default_start, default_end))
    with c3:
        timezone_offset = st.number_input(
            "時區偏移（台灣=8）",
            value=8,
            min_value=-12,
            max_value=14,
            step=1,
            help="填入與 UTC 的時差小時數，例如台灣 +8、日本 +9、UTC 0。",
        )
        time_unit = st.selectbox("時間單位", ["day", "hour"])

    submitted = st.form_submit_button("更新門店儀表板", type="primary", use_container_width=True)

if submitted:
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range

    base_query = {
        "start_time": to_unix(start_date, end_of_day=False, timezone_offset=int(timezone_offset)),
        "end_time": to_unix(end_date, end_of_day=True, timezone_offset=int(timezone_offset)),
        "timezone_offset": int(timezone_offset),
        "time_unit": time_unit,
    }

    one_shop_query = dict(base_query)
    if mode == "目前門店" and shop_id:
        one_shop_query["shop_id"] = shop_id

    shop_paging_query = dict(base_query)
    shop_paging_query.update({"limit": 200, "offset": 0})

    api_bundle = {
        "門店摘要": ("brief_shop", one_shop_query),
        "門店趨勢": ("analysis_shop", one_shop_query),
        "跨門店明細": ("analysis_shop_paging", shop_paging_query),
        "運行摘要": ("brief_run", one_shop_query),
        "門店列表": ("shop_list", {"limit": 200, "offset": 0}),
    }

    results = {title: call_api(api_id, query) for title, (api_id, query) in api_bundle.items()}
    st.session_state["_shop_results"] = results

results = st.session_state.get("_shop_results") or {}

if not results:
    st.info("請先按「更新門店儀表板」。")
    st.stop()

st.markdown("<div class='section-title'>核心 KPI（門店向）</div>", unsafe_allow_html=True)

kpi_pool: list[tuple[str, float]] = []
for key in ("門店摘要", "運行摘要"):
    payload = extract_payload(results.get(key, {}))
    if isinstance(payload, dict):
        summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else payload
        kpi_pool.extend(collect_numeric_items(summary))

seen = set()
kpi_items = []
for name, value in kpi_pool:
    short = name.split(".")[-1]
    if short in seen:
        continue
    seen.add(short)
    kpi_items.append((short, value))

cols = st.columns(4)
for idx, (name, value) in enumerate(kpi_items[:8]):
    with cols[idx % 4]:
        render_kpi(name, value)

left, right = st.columns(2)
with left:
    with st.container(border=True):
        st.markdown("**門店趨勢**")
        trend_result = results.get("門店趨勢", {})
        _render_status(trend_result)
        trend_payload = extract_payload(trend_result)
        status = int(trend_result.get("status_code") or 0)
        if 200 <= status < 300:
            blocks = find_chart_blocks(trend_payload)
            if not blocks:
                st.caption("目前沒有可繪圖資料")
            for idx, (path, rows) in enumerate(blocks[:2], start=1):
                render_line_or_bar(f"門店趨勢 圖 {idx} ({path})", rows)
            st.caption(
                "圖例顏色依欄位順序對應：藍色通常是 lively_count/活躍機器數、淺藍是 new_count/新增或當日有單機器數、"
                "綠色是 silent_count/靜默機器數、橘色是 total_count/總機器數。若門店只有 1 台機器，線條常只會落在 0 或 1。"
            )

with right:
    with st.container(border=True):
        st.markdown("**跨門店排行（柱狀圖）**")
        rank_result = results.get("跨門店明細", {})
        _render_status(rank_result)
        rank_payload = extract_payload(rank_result)
        if isinstance(rank_payload, dict) and isinstance(rank_payload.get("list"), list):
            rows = [r for r in rank_payload.get("list") if isinstance(r, dict)]
            if rows:
                candidates = [k for k in rows[0].keys() if any(isinstance(x.get(k), (int, float)) for x in rows)]
                metric_key = st.selectbox("排行欄位", candidates, key="shop_rank_metric") if candidates else None
                label_key = "shop_name" if "shop_name" in rows[0] else ("shop_id" if "shop_id" in rows[0] else None)
                if metric_key and label_key:
                    top_rows = sorted(rows, key=lambda x: float(x.get(metric_key) or 0), reverse=True)[:10]
                    render_line_or_bar(
                        f"Top 10 - {metric_key}",
                        [{"label": str(r.get(label_key) or "-"), "metric": float(r.get(metric_key) or 0)} for r in top_rows],
                        max_series=1,
                        height=380,
                    )
                    with st.expander("查看跨門店明細"):
                        st.dataframe(top_rows, use_container_width=True)
                else:
                    st.caption("跨門店明細缺少可用欄位")
            else:
                st.caption("跨門店明細目前為空")

st.markdown("<div class='section-title' style='margin-top:12px;'>門店清單</div>", unsafe_allow_html=True)
shop_list_result = results.get("門店列表", {})
with st.container(border=True):
    _render_status(shop_list_result)
    shop_payload = extract_payload(shop_list_result)
    if isinstance(shop_payload, list) and shop_payload:
        st.dataframe(shop_payload, use_container_width=True)
    elif isinstance(shop_payload, dict):
        list_data = shop_payload.get("list")
        if isinstance(list_data, list) and list_data:
            st.dataframe(list_data, use_container_width=True)
        else:
            st.caption("門店列表沒有資料")
    else:
        st.caption("門店列表沒有資料")

with st.expander("原始 API 回應（偵錯）"):
    st.json(results)
