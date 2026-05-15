from __future__ import annotations

import datetime as dt
import os
import sys

import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import services.repo as repo
from services.api_definitions import COMMON_APIS
from services.pudu_client import call_pudu


THEME_CSS = """
<style>
:root {
  --bg: #08101f;
  --panel: #0f1c35;
  --panel-2: #132748;
  --line: #21477f;
  --txt: #d8e8ff;
  --muted: #8fafda;
  --accent: #49b3ff;
}
.stApp {
  background: radial-gradient(circle at 20% 10%, #13294f 0%, #08101f 50%, #060c18 100%);
  color: var(--txt);
}
[data-testid="stForm"] {
  background: linear-gradient(160deg, rgba(15,28,53,0.95), rgba(9,20,40,0.95));
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 12px;
}
.kpi-card {
  background: linear-gradient(160deg, rgba(19,39,72,0.95), rgba(10,25,47,0.95));
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 12px;
  min-height: 88px;
}
.kpi-label { color: var(--muted); font-size: 12px; margin-bottom: 4px; }
.kpi-value { color: var(--txt); font-size: 24px; font-weight: 700; }
.section-title { color: var(--accent); font-weight: 700; font-size: 16px; }
</style>
"""


def ensure_authenticated(page_title: str, page_icon: str) -> None:
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")
    if not st.session_state.get("authenticated"):
        st.warning("請先登入")
        st.stop()
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def _iter_common_apis():
    for _, apis in COMMON_APIS.items():
        for api in apis:
            yield api


def get_api(api_id: str) -> dict | None:
    return next((api for api in _iter_common_apis() if str(api.get("id") or "") == api_id), None)


def call_api(api_id: str, query: dict) -> dict:
    api = get_api(api_id)
    if not api:
        return {"status_code": 0, "url": "", "json": None, "text": f"找不到 API: {api_id}"}
    try:
        return call_pudu(
            str(api.get("method") or "GET"),
            str(api.get("path") or ""),
            query=query,
            body=None,
            return_raw=True,
        )
    except Exception as exc:
        return {"status_code": 0, "url": str(api.get("path") or ""), "json": None, "text": str(exc)}


def to_unix(value: dt.date, *, end_of_day: bool, timezone_offset: int) -> int:
    tz = dt.timezone(dt.timedelta(hours=int(timezone_offset)))
    if end_of_day:
        val = dt.datetime(value.year, value.month, value.day, 23, 59, 59, tzinfo=tz)
    else:
        val = dt.datetime(value.year, value.month, value.day, 0, 0, 0, tzinfo=tz)
    return int(val.timestamp())


def numeric(v: object) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def extract_payload(result: dict) -> object:
    payload = result.get("json")
    if isinstance(payload, dict) and "data" in payload:
        return payload.get("data")
    return payload


def sn_of_row(row: dict) -> str:
    for key in ("sn", "robot_sn", "robotSn", "device_sn"):
        val = str(row.get(key) or "").strip()
        if val:
            return val
    return ""


def filter_sns(node: object, sns: set[str]) -> object:
    if not sns:
        return node
    if isinstance(node, list):
        out = []
        for item in node:
            if isinstance(item, dict):
                sn = sn_of_row(item)
                if sn and sn not in sns:
                    continue
                out.append({k: filter_sns(v, sns) for k, v in item.items()})
            else:
                out.append(filter_sns(item, sns))
        return out
    if isinstance(node, dict):
        return {k: filter_sns(v, sns) for k, v in node.items()}
    return node


def pick_x(rows: list[dict]) -> str | None:
    preferred = ["task_time", "time", "date", "day", "hour", "label", "name", "type", "x"]
    keys = set()
    for row in rows:
        keys.update(row.keys())
    for key in preferred:
        if key in keys:
            return key
    for key in keys:
        vals = [row.get(key) for row in rows if row.get(key) is not None]
        if vals and all(not numeric(v) for v in vals):
            return key
    return None


def find_chart_blocks(node: object, prefix: str = "data") -> list[tuple[str, list[dict]]]:
    found: list[tuple[str, list[dict]]] = []
    if isinstance(node, list) and node and all(isinstance(item, dict) for item in node):
        rows = [item for item in node if isinstance(item, dict)]
        if rows:
            x_key = pick_x(rows)
            numeric_keys = {k for row in rows for k, v in row.items() if numeric(v)}
            if x_key and numeric_keys:
                found.append((prefix, rows))
    if isinstance(node, dict):
        for key, value in node.items():
            found.extend(find_chart_blocks(value, f"{prefix}.{key}"))
    elif isinstance(node, list):
        for idx, item in enumerate(node[:8]):
            found.extend(find_chart_blocks(item, f"{prefix}[{idx}]"))
    return found


def collect_numeric_items(node: object, prefix: str = "") -> list[tuple[str, float]]:
    out: list[tuple[str, float]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            name = f"{prefix}.{key}" if prefix else key
            if numeric(value):
                out.append((name, float(value)))
            elif isinstance(value, (dict, list)):
                out.extend(collect_numeric_items(value, name))
    return out


def render_kpi(label: str, value: object) -> None:
    display = "-"
    if isinstance(value, float):
        display = f"{value:,.2f}"
    elif isinstance(value, int):
        display = f"{value:,}"
    elif value not in (None, ""):
        display = str(value)
    st.markdown(
        f"<div class='kpi-card'><div class='kpi-label'>{label}</div><div class='kpi-value'>{display}</div></div>",
        unsafe_allow_html=True,
    )


def render_line_or_bar(title: str, rows: list[dict], *, max_series: int = 4, height: int = 300) -> None:
    x_key = pick_x(rows)
    if not x_key:
        st.caption("無法判斷 X 軸欄位")
        return
    numeric_keys = [k for k in rows[0].keys() if any(numeric(row.get(k)) for row in rows)]
    if not numeric_keys:
        st.caption("無可繪圖數值欄位")
        return

    colors = ["#49b3ff", "#ff6b6b", "#39d98a", "#f5a524"]
    fig = go.Figure()
    x_vals = [row.get(x_key) for row in rows]
    for idx, key in enumerate(numeric_keys[:max_series]):
        y_vals = [row.get(key) for row in rows]
        if len(numeric_keys) == 1:
            fig.add_trace(go.Bar(x=x_vals, y=y_vals, name=key, marker_color=colors[idx % len(colors)], opacity=0.9))
        else:
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode="lines+markers",
                    name=key,
                    line=dict(width=2, color=colors[idx % len(colors)]),
                    marker=dict(size=5),
                )
            )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        height=height,
        margin=dict(l=16, r=16, t=40, b=16),
        title=dict(text=title, font=dict(size=13, color="#a7cfff")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)", tickformat="d", dtick=1),
    )
    st.plotly_chart(fig, use_container_width=True)


def load_store_context() -> tuple[dict, list[dict], list[dict], dict[str, dict]]:
    store = repo.get_or_create_default_store()
    store_id = store.get("id")
    robots = repo.list_robots(store_id) if store_id else []
    groups = repo.list_groups(store_id) if store_id else []
    robot_map = {str(r.get("id") or ""): r for r in robots}
    return store, robots, groups, robot_map


def build_group_robot_options(groups: list[dict], robot_map: dict[str, dict], include_keywords: list[str]) -> dict[str, str]:
    lower_keys = [k.lower() for k in include_keywords]
    target_groups = []
    for g in groups:
        name = str(g.get("name") or "").strip()
        if not name or name.startswith("_"):
            continue
        if any(k in name.lower() for k in lower_keys):
            target_groups.append(g)

    sns: list[str] = []
    for g in target_groups:
        for rid in g.get("robot_ids") or []:
            r = robot_map.get(str(rid))
            if not r:
                continue
            sn = str(r.get("sn") or "").strip()
            if sn and sn not in sns and r.get("is_enabled"):
                sns.append(sn)

    options: dict[str, str] = {}
    for sn in sns:
        options[sn] = sn
    return options


def build_all_enabled_robot_options(robots: list[dict]) -> dict[str, str]:
    options: dict[str, str] = {}
    for r in robots:
        if not r.get("is_enabled"):
            continue
        sn = str(r.get("sn") or "").strip()
        if not sn:
            continue
        nickname = str(r.get("nickname") or "").strip()
        label = f"{nickname}（{sn}）" if nickname else sn
        options[label] = sn
    return options
